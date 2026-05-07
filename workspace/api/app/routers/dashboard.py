"""
Dashboard Router - /api/v1/dashboard/*

M6-API-07: All DB access is delegated to Repositories. Router never executes
SQL directly. Session is only injected to construct repos.
"""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.auth import UserContext, current_user
from app.deps.db import get_async_session
from app.repositories.customer_repo import CustomerRepository
from app.repositories.project_repo import ProjectRepository
from app.repositories.task_repo import TaskRepository

router = APIRouter()


@router.get("/summary")
async def dashboard_summary(
    user: UserContext = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    task_repo = TaskRepository(session)
    project_repo = ProjectRepository(session)
    customer_repo = CustomerRepository(session)

    return {
        "task_count": await task_repo.count_by_assignee(user.id),
        "project_count": await project_repo.count_by_owner(user.id),
        "customer_count": await customer_repo.count_active(),
        "pending_tasks": 0,
    }


@router.get("/recent-tasks")
async def recent_tasks(
    limit: int = 10,
    user: UserContext = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    task_repo = TaskRepository(session)
    tasks = await task_repo.list_recent_by_assignee(user.id, limit)
    return [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "priority": t.priority,
            "gmt_create": t.gmt_create.isoformat(),
        }
        for t in tasks
    ]


@router.get("/recent-projects")
async def recent_projects(
    limit: int = 5,
    user: UserContext = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    project_repo = ProjectRepository(session)
    projects = await project_repo.list_recent_by_owner(user.id, limit)
    return [
        {"id": p.id, "name": p.name, "phase": p.phase, "health": p.health}
        for p in projects
    ]


@router.get("/notifications")
async def notifications(page: int = 1, size: int = 10, user: UserContext = Depends(current_user)):
    return {"items": [], "total": 0}


@router.get("/key-events")
async def key_events(
    days: int = Query(7, ge=1, le=365, description="时间范围天数，1-365，默认7天"),
    user: UserContext = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    task_repo = TaskRepository(session)
    since = datetime.utcnow() - timedelta(days=days)
    tasks = await task_repo.list_created_since(user.id, since)
    return [
        {
            "id": t.id,
            "type": "task_created",
            "title": t.title,
            "gmt_create": t.gmt_create.isoformat(),
        }
        for t in tasks
    ]
