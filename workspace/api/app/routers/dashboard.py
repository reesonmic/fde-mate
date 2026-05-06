"""
Dashboard Router - /api/v1/dashboard/*
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_async_session
from app.deps.auth import UserContext, current_user
from app.models.task import Task
from app.models.project import Project
from app.models.customer import Customer

router = APIRouter()


@router.get("/summary")
async def dashboard_summary(user: UserContext = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    task_count = await session.scalar(
        select(func.count()).where(Task.is_deleted == 0, Task.assignee_id == user.id)
    )
    project_count = await session.scalar(
        select(func.count()).where(Project.is_deleted == 0, Project.owner_id == user.id)
    )
    customer_count = await session.scalar(
        select(func.count()).where(Customer.is_deleted == 0)
    )
    return {
        "task_count": task_count or 0,
        "project_count": project_count or 0,
        "customer_count": customer_count or 0,
        "pending_tasks": 0,
    }


@router.get("/recent-tasks")
async def recent_tasks(limit: int = 10, user: UserContext = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(Task).where(Task.is_deleted == 0, Task.assignee_id == user.id)
        .order_by(Task.gmt_create.desc()).limit(limit)
    )
    tasks = result.scalars().all()
    return [
        {
            "id": t.id, "title": t.title, "status": t.status,
            "priority": t.priority, "gmt_create": t.gmt_create.isoformat(),
        }
        for t in tasks
    ]


@router.get("/recent-projects")
async def recent_projects(limit: int = 5, user: UserContext = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(Project).where(Project.is_deleted == 0, Project.owner_id == user.id)
        .order_by(Project.gmt_create.desc()).limit(limit)
    )
    projects = result.scalars().all()
    return [
        {"id": p.id, "name": p.name, "phase": p.phase, "health": p.health}
        for p in projects
    ]


@router.get("/notifications")
async def notifications(page: int = 1, size: int = 10, user: UserContext = Depends(current_user)):
    return {"items": [], "total": 0}


@router.get("/key-events")
async def key_events(days: int = 7, user: UserContext = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    since = datetime.utcnow() - timedelta(days=days)
    result = await session.execute(
        select(Task).where(Task.is_deleted == 0, Task.assignee_id == user.id, Task.gmt_create >= since)
        .order_by(Task.gmt_create.desc()).limit(20)
    )
    tasks = result.scalars().all()
    return [
        {"id": t.id, "type": "task_created", "title": t.title, "gmt_create": t.gmt_create.isoformat()}
        for t in tasks
    ]
