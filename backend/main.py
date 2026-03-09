from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from api import auth, tasks, notifications
from core.scheduler import start_scheduler, stop_scheduler

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    try:
        yield
    finally:
        stop_scheduler()


app = FastAPI(title="Schedulix.io", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(notifications.router)

@app.get("/health")
async def healthcheck():
    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
