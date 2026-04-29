"""
FastAPI Application Entry Point
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.config.logging import setup_logging
from app.middleware.trace import TraceMiddleware
from app.middleware.logging import LoggingMiddleware
from app.exceptions.handlers import setup_exception_handlers
from app.routers import auth, dashboard, tasks, projects, customers, files, coach, copilot, mentions, settings_router

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    description="FDE Workbench Backend API",
    version="0.1.0",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TraceMiddleware)
app.add_middleware(LoggingMiddleware)

# Exception handlers
setup_exception_handlers(app)

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(customers.router, prefix="/api/v1/customers", tags=["customers"])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
app.include_router(coach.router, prefix="/api/v1/coach", tags=["coach"])
app.include_router(copilot.router, prefix="/api/v1/copilot", tags=["copilot"])
app.include_router(mentions.router, prefix="/api/v1/mentions", tags=["mentions"])
app.include_router(settings_router.router, prefix="/api/v1/settings", tags=["settings"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}