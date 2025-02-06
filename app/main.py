import asyncio
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from app.core.database import db
from app.routes.auth import auth_router
from app.routes.cv_router import cv_router
from app.services.job_fetch_service import JobFetchService

app = FastAPI(title="CV Processing API", version="2.0.0")
static_dir = Path(__file__).parent.parent / "static"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(cv_router, prefix="/cv", tags=["CV Processing"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")


@app.on_event("startup")
async def startup_event():
    await db.connect()
    asyncio.create_task(schedule_job_fetching())


@app.on_event("shutdown")
async def shutdown_event():
    await db.disconnect()


@app.get("/")
async def read_index():
    return FileResponse(static_dir / "index.html")


@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "Service is up and running"}


async def schedule_job_fetching():
    """Runs job fetching every 24 hours in the background."""
    while True:
        try:
            print("Fetching new jobs from RSS feed...")
            await JobFetchService.fetch_and_store_jobs()  # Ensure this is awaited
            print("Job fetching completed.")
        except Exception as e:
            print(f"Error fetching jobs: {str(e)}")

        await asyncio.sleep(86400)  # Wait 24 hours (86400 seconds) before next fetch
