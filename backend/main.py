from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from dotenv import load_dotenv
from api import auth, tasks, pages, notifications

load_dotenv()

app = FastAPI(title="Schedulix.io")
from fastapi.staticfiles import StaticFiles

# class NoCacheStaticFiles(StaticFiles):
#     async def get_response(self, path, scope):
#         response = await super().get_response(path, scope)
#         response.headers["Cache-Control"] = "no-store"
#         return response

# app.mount("/static", NoCacheStaticFiles(directory="static"), name="static")

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Routers
# app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(notifications.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
