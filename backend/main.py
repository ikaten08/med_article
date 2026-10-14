# backend/main.py

"""FastAPI application entry point.
The app mounts API routes under `/api` and serves a minimal static front‑end
from the `frontend` directory. On startup the database tables are created
if they do not exist.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Import routers (they register themselves with the app)
from .routers import papers

# Import DB Base to create tables on startup
from .models import Base
from .database import engine

app = FastAPI(title="MedLearn MVP")

# Create tables (idempotent)
Base.metadata.create_all(bind=engine)

# Include API router with prefix /api
app.include_router(papers.router, prefix="/api")

# Serve static front‑end (index.html etc.)
frontend_path = Path(__file__).parents[1] / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
