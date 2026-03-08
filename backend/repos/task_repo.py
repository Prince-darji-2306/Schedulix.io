from repos.database import get_db_connection
import json
from psycopg2.extras import RealDictCursor
from datetime import datetime, date, time
import copy
import threading
from time import time as now_ts

CACHE_TTL_SECONDS = 60
_CACHE = {}
_CACHE_LOCK = threading.Lock()


def _cache_get(key: str):
    with _CACHE_LOCK:
        item = _CACHE.get(key)
        if not item:
            return None

        expires_at, value = item
        if expires_at < now_ts():
            _CACHE.pop(key, None)
            return None

        return copy.deepcopy(value)


def _cache_set(key: str, value, ttl_seconds: int = CACHE_TTL_SECONDS):
    with _CACHE_LOCK:
        _CACHE[key] = (now_ts() + ttl_seconds, copy.deepcopy(value))


def _cache_invalidate_prefix(prefix: str):
    with _CACHE_LOCK:
        keys_to_delete = [key for key in _CACHE.keys() if key.startswith(prefix)]
        for key in keys_to_delete:
            _CACHE.pop(key, None)


def _invalidate_task_related_cache(user_id: int):
    _cache_invalidate_prefix(f"tasks:{user_id}:")
    _cache_invalidate_prefix(f"routine:{user_id}:")
    _cache_invalidate_prefix(f"notifications:{user_id}:")


def _invalidate_notifications_cache(user_id: int):
    _cache_invalidate_prefix(f"notifications:{user_id}:")

def get_tasks_by_user(user_id: int):
    cache_key = f"tasks:{user_id}:all"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
        SELECT 
            id,
            title,
            description,
            ai_plan_json,
            plan_approved,
            deadline_date,
            time,
            CASE 
                WHEN status != 'completed' AND (deadline_date + time) < NOW()
                    THEN 'overdue'
                ELSE status
            END AS status
        FROM tasks
        WHERE user_id = %s
        ORDER BY
            CASE 
                WHEN status != 'completed' AND (deadline_date + time) < NOW() THEN 1  -- Overdue
                WHEN status = 'pending' THEN 2                          -- Pending
                WHEN status = 'completed' THEN 3                        -- Completed
                ELSE 4
            END,
            deadline_date ASC, time ASC;
        """
        cursor.execute(query, (user_id,))
        tasks = cursor.fetchall()
        for task in tasks:
            # Convert date and time objects to string for JSON serialization
            if task['deadline_date']:
                 task['deadline_date'] = str(task['deadline_date'])
            else:
                 task['deadline_date'] = 'N/A'
                 
            if task['time']:
                 task['time'] = str(task['time'])
            else:
                 task['time'] = '00:00:00'
            
            # psycopg2 might return JSONB as a dict already
            if isinstance(task['ai_plan_json'], str):
                try:
                    task['ai_plan_json'] = json.loads(task['ai_plan_json'])
                except:
                    task['ai_plan_json'] = {"error": "Invalid plan format"}
            elif task['ai_plan_json'] is None:
                task['ai_plan_json'] = None
            
        _cache_set(cache_key, tasks)
        return tasks
    finally:
        cursor.close()
        conn.close()

def create_task_record(title: str, description: str, user_id: int, deadline_date: str, time: str, status: str, ai_plan_json: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO tasks (title, description, user_id, deadline_date, time, status, ai_plan_json) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (title, description, user_id, deadline_date, time, status.lower(), ai_plan_json)
        )
        conn.commit()
        _invalidate_task_related_cache(user_id)
        return True
    finally:
        cursor.close()
        conn.close()

def get_tasks_for_today(user_id: int, today_str: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = "SELECT title, description, ai_plan_json, deadline_date, time FROM tasks WHERE user_id = %s AND deadline_date = %s"
        cursor.execute(query, (user_id, today_str))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# --- Subtasks Methods ---
def create_subtask(task_id: int, subtask: str, description: str, time_to: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO subtasks (task_id, subtask, description, time_to) VALUES (%s, %s, %s, %s)",
            (task_id, subtask, description, time_to)
        )
        cursor.execute("SELECT user_id FROM tasks WHERE id = %s", (task_id,))
        row = cursor.fetchone()
        conn.commit()

        if row:
            _invalidate_task_related_cache(row[0])
    finally:
        cursor.close()
        conn.close()

def get_subtasks_for_today_all(user_id: int, today_str: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            SELECT s.*, t.title as task_title 
            FROM subtasks s 
            JOIN tasks t ON s.task_id = t.id 
            WHERE t.user_id = %s AND t.deadline_date = %s
            ORDER BY s.time_to ASC
        """
        cursor.execute(query, (user_id, today_str))
        subtasks = cursor.fetchall()
        for st in subtasks:
            if st['time_to']:
                st['time_to'] = str(st['time_to'])
        return subtasks
    finally:
        cursor.close()
        conn.close()

def update_subtask_status(subtask_id: int, is_completed: bool):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE subtasks
            SET is_completed = %s
            WHERE id = %s
            RETURNING task_id
            """,
            (is_completed, subtask_id)
        )
        task_row = cursor.fetchone()

        user_row = None
        if task_row:
            cursor.execute("SELECT user_id FROM tasks WHERE id = %s", (task_row[0],))
            user_row = cursor.fetchone()

        conn.commit()

        if user_row:
            _invalidate_task_related_cache(user_row[0])
    finally:
        cursor.close()
        conn.close()

def get_hierarchical_routine(user_id: int, today_str: str):
    cache_key = f"routine:{user_id}:{today_str}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Fetch tasks that are not completed and have a deadline today
        query_tasks = """
            SELECT id, title, description, status 
            FROM tasks 
            WHERE user_id = %s AND deadline_date = %s AND status != 'completed'
        """
        cursor.execute(query_tasks, (user_id, today_str))
        tasks = cursor.fetchall()
        
        for task in tasks:
            # Fetch subtasks for each task
            query_subtasks = "SELECT * FROM subtasks WHERE task_id = %s ORDER BY time_to ASC"
            cursor.execute(query_subtasks, (task['id'],))
            subtasks = cursor.fetchall()
            for st in subtasks:
                if st['time_to']:
                    st['time_to'] = str(st['time_to'])
            task['subtasks'] = subtasks
            
        _cache_set(cache_key, tasks)
        return tasks
    finally:
        cursor.close()
        conn.close()

def check_and_update_task_status(subtask_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Get task_id for the subtask
        cursor.execute("SELECT task_id FROM subtasks WHERE id = %s", (subtask_id,))
        res = cursor.fetchone()
        if not res: return
        task_id = res['task_id']
        
        # Check if all subtasks for this task are completed
        cursor.execute("SELECT COUNT(*) as total FROM subtasks WHERE task_id = %s", (task_id,))
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as completed FROM subtasks WHERE task_id = %s AND is_completed = TRUE", (task_id,))
        completed = cursor.fetchone()['completed']
        
        if total > 0 and total == completed:
            update_task_status(task_id, 'completed')
            return True
        else:
            # If not all are completed, ensure it's not marked as 'completed'
            cursor.execute("SELECT status FROM tasks WHERE id = %s", (task_id,))
            res_status = cursor.fetchone()
            if res_status:
                current_status = res_status['status']
                if current_status == 'completed':
                    update_task_status(task_id, 'pending')
        return False
    finally:
        cursor.close()
        conn.close()

def update_task_status(task_id: int, status: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tasks SET status = %s WHERE id = %s RETURNING user_id", (status.lower(), task_id))
        row = cursor.fetchone()
        conn.commit()

        if row:
            _invalidate_task_related_cache(row[0])
    finally:
        cursor.close()
        conn.close()

def update_plan_approval_status(task_id: int, approved: bool):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE tasks SET plan_approved = %s WHERE id = %s RETURNING user_id", (approved, task_id))
        row = cursor.fetchone()
        conn.commit()

        if row:
            _invalidate_task_related_cache(row[0])
    finally:
        cursor.close()
        conn.close()

# --- Notifications Methods ---
def get_user_notifications(user_id: int):
    cache_key = f"notifications:{user_id}:all"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        notifications = cursor.fetchall()
        for note in notifications:
            if note['created_at']:
                note['created_at'] = note['created_at'].strftime("%Y-%m-%d %H:%M")

        _cache_set(cache_key, notifications)
        return notifications
    finally:
        cursor.close()
        conn.close()

def mark_note_as_read(note_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE notifications SET is_read = TRUE WHERE id = %s RETURNING user_id", (note_id,))
        row = cursor.fetchone()
        conn.commit()

        if row:
            _invalidate_notifications_cache(row[0])
    finally:
        cursor.close()
        conn.close()

def create_user_notification(user_id: int, message: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO notifications (user_id, message) VALUES (%s, %s)", (user_id, message))
        conn.commit()
        _invalidate_notifications_cache(user_id)
    finally:
        cursor.close()
        conn.close()
