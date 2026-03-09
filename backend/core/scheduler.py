import os
import psycopg2
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

scheduler = BackgroundScheduler()


def update_overdue_tasks() -> None:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE tasks
            SET status = 'overdue'
            WHERE deadline_date < CURRENT_DATE
              AND status != 'completed';
            """
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def start_scheduler() -> None:
    if scheduler.running:
        return
    scheduler.add_job(
        update_overdue_tasks,
        trigger="cron",
        hour="9,21",
        id="update_overdue_tasks_twice_daily",
        replace_existing=True,
    )
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
