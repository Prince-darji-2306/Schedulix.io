from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from api import auth, tasks, notifications

load_dotenv()

app = FastAPI(
    title="Schedulix.io API",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

@app.get("/health")
async def health_check():
    return {"status": "success"}


@app.get("/health/docs")
async def health_docs_check():
    return {
        "status": "success",
        "docs_available": True,
        "docs_url": "/docs"
    }

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers (API Only)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(notifications.router)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
