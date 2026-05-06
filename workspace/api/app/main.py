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
from app.routers.auth import router as auth_router
from app.routers.dashboard import router as dashboard_router
from app.routers.tasks import router as tasks_router
from app.routers.projects import router as projects_router
from app.routers.customers import router as customers_router
from app.routers.files import router as files_router
from app.routers.coach import router as coach_router
from app.routers.copilot import router as copilot_router
from app.routers.mentions import router as mentions_router
from app.routers.settings import router as settings_router

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
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(projects_router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(customers_router, prefix="/api/v1/customers", tags=["customers"])
app.include_router(files_router, prefix="/api/v1/files", tags=["files"])
app.include_router(coach_router, prefix="/api/v1/coach", tags=["coach"])
app.include_router(copilot_router, prefix="/api/v1/copilot", tags=["copilot"])
app.include_router(mentions_router, prefix="/api/v1/mentions", tags=["mentions"])
app.include_router(settings_router, prefix="/api/v1/settings", tags=["settings"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}