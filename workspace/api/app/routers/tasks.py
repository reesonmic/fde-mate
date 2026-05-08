"""
Tasks Router - /api/v1/tasks/*
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_async_session
from app.deps.auth import UserContext, current_user
from app.repositories.task_repo import TaskRepository
from app.services.task_service import TaskService
from app.services.action_service import ActionService
from app.schemas.task import (
    TaskDTO, TaskCreate, TaskUpdate, TaskQuery,
    BatchUpdateStatusRequest, BatchAssignRequest,
    TaskHistoryDTO,
)

router = APIRouter()


def get_task_service(session: AsyncSession = Depends(get_async_session)) -> TaskService:
    repo = TaskRepository(session)
    action_svc = ActionService()
    return TaskService(session, repo, action_svc)


@router.get("")
async def list_tasks(query: TaskQuery = Depends(), svc: TaskService = Depends(get_task_service), user: UserContext = Depends(current_user)):
    return await svc.list_tasks(query, user.id)


@router.get("/{task_id}", response_model=TaskDTO)
async def get_task(task_id: int, svc: TaskService = Depends(get_task_service), user: UserContext = Depends(current_user)):
    return await svc.get_task(task_id, user.id)


@router.post("", response_model=TaskDTO)
async def create_task(payload: TaskCreate, svc: TaskService = Depends(get_task_service), user: UserContext = Depends(current_user)):
    return await svc.create_task(payload, user.id)


@router.put("/{task_id}", response_model=TaskDTO)
async def update_task(task_id: int, payload: TaskUpdate, svc: TaskService = Depends(get_task_service), user: UserContext = Depends(current_user)):
    return await svc.update_task(task_id, payload, user.id)


@router.delete("/{task_id}")
async def delete_task(task_id: int, svc: TaskService = Depends(get_task_service), user: UserContext = Depends(current_user)):
    return await svc.delete_task(task_id, user.id)


@router.post("/batch-update-status")
async def batch_update_status(req: BatchUpdateStatusRequest, svc: TaskService = Depends(get_task_service), user: UserContext = Depends(current_user)):
    return await svc.batch_update_status(req, user.id)


@router.post("/batch-assign")
async def batch_assign(req: BatchAssignRequest, svc: TaskService = Depends(get_task_service), user: UserContext = Depends(current_user)):
    return await svc.batch_assign(req, user.id)


@router.get("/{task_id}/history", response_model=list[TaskHistoryDTO])
async def get_task_history(task_id: int, svc: TaskService = Depends(get_task_service), user: UserContext = Depends(current_user)):
    return await svc.get_history(task_id, user.id)
