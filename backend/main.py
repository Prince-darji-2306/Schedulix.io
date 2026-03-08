from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from api import auth, tasks, notifications

load_dotenv()

app = FastAPI(title="Schedulix.io")

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(notifications.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
