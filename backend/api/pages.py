from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/tasks", response_class=HTMLResponse)
async def get_tasks(request: Request):
    return templates.TemplateResponse("tasks_todo.html", {"request": request})

@router.get("/add-task", response_class=HTMLResponse)
async def get_add_task(request: Request):
    return templates.TemplateResponse("add_task.html", {"request": request})

@router.get("/routine", response_class=HTMLResponse)
async def get_daily_routine_page(request: Request):
    return templates.TemplateResponse("routine.html", {"request": request})

@router.get("/notifications", response_class=HTMLResponse)
async def get_notifications_page(request: Request):
    return templates.TemplateResponse("notifications.html", {"request": request})
