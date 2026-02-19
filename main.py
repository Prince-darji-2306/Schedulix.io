from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import mysql.connector
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional, List, TypedDict
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
import json

load_dotenv()

app = FastAPI(title="Schedulix.io")

# --- LangGraph AI Plan Generation ---
class PlanState(TypedDict):
    title: str
    description: str
    plans: List[str]
    final_plan: str

def generate_plans_node(state: PlanState):
    llm = ChatGroq(model_name="openai/gpt-oss-20b", temperature=0.7)
    prompt = (
        f"Generate 3 diverse and distinct plans for the following task:\n"
        f"Title: {state['title']}\n"
        f"Description: {state['description']}\n"
        f"Make sure they are truly different (e.g., one fast, one thorough, one creative).\n"
        f"List them clearly."
    )
    response = llm.invoke(prompt)
    return {"plans": [response.content]} # Simplification: LLM returns all 3 in content

def finalize_plan_node(state: PlanState):
    llm = ChatGroq(model_name="openai/gpt-oss-20b")
    prompt = (
        f"Based on these ideas:\n{state['plans'][0]}\n"
        f"Create a single, optimized, and comprehensive finalized plan for the task: {state['title']}."
    )
    response = llm.invoke(prompt)
    return {"final_plan": response.content}

# Create Graph
workflow = StateGraph(PlanState)
workflow.add_node("generator", generate_plans_node)
workflow.add_node("finalizer", finalize_plan_node)
workflow.set_entry_point("generator")
workflow.add_edge("generator", "finalizer")
workflow.add_edge("finalizer", END)
ai_graph = workflow.compile()

# --- Configuration ---
SECRET_KEY = "Thisismysecret" # In production, use env variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- Database Connection ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='task_planner'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise HTTPException(status_code=500, detail="Database connection failed")


# --- Initialize DB ---
def init_db():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="")
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS task_planner")
        cursor.execute("USE task_planner")
        # Ensure users table exists (Standardized name)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            )
        """)
        # Create tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                user_id INT,
                deadline DATETIME,
                status VARCHAR(50) DEFAULT 'Pending',
                ai_plan_json JSON,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"DB Init Error: {e}")

init_db()

# --- Auth Utilities ---
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        # Remove "Bearer " if present
        if token.startswith("Bearer "):
            token = token[7:]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- Routes ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/tasks", response_class=HTMLResponse)
async def get_tasks(request: Request):
    return templates.TemplateResponse("tasks_todo.html", {"request": request})

@app.get("/add-task", response_class=HTMLResponse)
async def get_add_task(request: Request):
    return templates.TemplateResponse("add_task.html", {"request": request})

# --- API Endpoints ---
@app.post("/api/register")
async def register(request: Request):
    data = await request.json()
    username = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        raise HTTPException(status_code=400, detail="All fields are required")

    hashed_pw = hash_password(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hashed_pw)
        )
        conn.commit()
        return {"status": "success", "message": "User registered successfully"}
    except mysql.connector.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or Email already exists")
    finally:
        cursor.close()
        conn.close()

@app.post("/api/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and verify_password(password, user['password_hash']):
        token = create_access_token({"sub": user['username'], "email": user['email'], "id": user['id']})
        return {"status": "success", "access_token": token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/tasks")
async def create_task(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Not authorized")
    
    payload = decode_token(token)
    user_id = payload.get("id")
    
    data = await request.json()
    title = data.get("title")
    description = data.get("description")
    deadline = data.get("deadline")
    status = data.get("status", "Pending")
    print(status)
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    # AI Plan Generation using LangGraph
    try:
        # Prompting for 3 diverse plans and combining them is handled in the graph nodes
        ai_result = await ai_graph.ainvoke({
            "title": title, 
            "description": description,
            "plans": [],
            "final_plan": ""
        })
        ai_plan_data = {"final_plan": ai_result["final_plan"]}
        ai_plan_json = json.dumps(ai_plan_data)
    except Exception as e:
        print(f"AI Generation Error: {e}")
        ai_plan_json = json.dumps({"error": "AI planning failed", "details": str(e)})

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tasks (title, description, user_id, deadline, status, ai_plan_json) VALUES (%s, %s, %s, %s, %s, %s)",
            (title, description, user_id, deadline, status, ai_plan_json)
        )
        conn.commit()
        return {"status": "success", "message": "Task and AI Plan created successfully"}
    except Exception as e:
        print(f"Task Creation Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create task")
    finally:
        cursor.close()
        conn.close()

@app.get("/routine", response_class=HTMLResponse)
async def get_daily_routine_page(request: Request):
    return templates.TemplateResponse("routine.html", {"request": request})

@app.get("/api/routine")
async def get_daily_routine_data(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Not authorized")
    
    payload = decode_token(token)
    user_id = payload.get("id")

    # Fetch tasks for today
    today = datetime.now().strftime("%Y-%m-%d")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Fetch tasks that are either for today or pending
        query = "SELECT title, description, ai_plan_json, deadline FROM tasks WHERE user_id = %s AND DATE(deadline) = %s"
        cursor.execute(query, (user_id, today))
        tasks = cursor.fetchall()

        if not tasks:
            return {"routine": [], "message": "No tasks scheduled for today!"}

        # Prepare prompt for AI
        tasks_list = []
        for t in tasks:
            plan_text = ""
            if t['ai_plan_json']:
                try:
                    plan_data = json.loads(t['ai_plan_json'])
                    plan_text = f" (Plan: {plan_data.get('final_plan', 'None')})"
                except:
                    pass
            tasks_list.append(f"- {t['title']} (Desc: {t['description']}){plan_text}")
        
        tasks_str = "\n".join(tasks_list)
        
        prompt = (
            f"I have these tasks for today, some with specific AI-generated strategies:\n{tasks_str}\n\n"
            f"Current date: {today}\n"
            f"Create a timed daily routine schedule in JSON format. "
            f"Each item should have 'time' (e.g. '09:00 AM'), 'task' (short title), and 'description' (detail on what to do based on the provided plans)."
            f"Return ONLY a JSON array of objects."
        )

        llm = ChatGroq(model_name="openai/gpt-oss-20b")
        response = llm.invoke(prompt)
        
        # Extract JSON from response
        try:
            # Basic cleaning if LLM adds markdown backticks
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
            
            routine_data = json.loads(content)
            return {"routine": routine_data}
        except Exception as e:
            print(f"JSON Parse Error: {e}")
            return {"routine": [], "error": "AI failed to format routine properly."}
            
    finally:
        cursor.close()
        conn.close()

@app.get("/api/tasks")
async def get_all_tasks(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Not authorized")
    
    payload = decode_token(token)
    user_id = payload.get("id")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM tasks WHERE user_id = %s ORDER BY deadline DESC", (user_id,))
        tasks = cursor.fetchall()
        for task in tasks:
            if task['deadline']:
                task['deadline'] = task['deadline'].strftime("%Y-%m-%d %H:%M")
            if task['ai_plan_json']:
                try:
                    task['ai_plan_json'] = json.loads(task['ai_plan_json'])
                except:
                    task['ai_plan_json'] = {"error": "Invalid plan format"}
        return tasks
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
