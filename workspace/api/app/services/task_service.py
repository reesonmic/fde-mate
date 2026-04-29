"""
Task Service - CRUD + batch + history.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.biz import TaskNotFoundException, PermissionDeniedException
from app.exceptions.codes import BIZ_TASK_NOT_FOUND, BIZ_NO_TASK_PERMISSION, BIZ_AI_ACTION_REQUIRED
from app.models.task import Task
from app.repositories.task_repo import TaskRepository
from app.schemas.common import PageResponse
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskDTO, TaskQuery,
    BatchUpdateStatusRequest, BatchAssignRequest,
    TaskCommentCreate, TaskCommentDTO, TaskHistoryDTO,
)
from app.services.action_service import ActionService


class TaskService:
    def __init__(self, session: AsyncSession, repo: TaskRepository, action_svc: ActionService):
        self.session = session
        self.repo = repo
        self.action_svc = action_svc

    async def list_tasks(self, query: TaskQuery, user_id: int) -> PageResponse[TaskDTO]:
        items, total = await self.repo.search(
            keyword=query.keyword,
            status=[s.value for s in query.status] if query.status else None,
            assignee_id=query.assignee_id,
            project_id=query.project_id,
            priority=[p.value for p in query.priority] if query.priority else None,
            viewer_id=user_id,
            page=query.page,
            size=query.size,
        )
        return PageResponse(
            items=[TaskDTO.model_validate(t, from_attributes=True) for t in items],
            total=total, page=query.page, size=query.size,
        )

    async def get_task(self, task_id: int, user_id: int) -> TaskDTO:
        task = await self.repo.get(task_id)
        if not task or task.is_deleted:
            raise TaskNotFoundException()
        await self._check_read_access(task, user_id)
        return TaskDTO.model_validate(task, from_attributes=True)

    async def create_task(self, payload: TaskCreate, user_id: int) -> TaskDTO:
        task = await self.repo.create_task(
            title=payload.title,
            description=payload.description,
            status=payload.status.value,
            priority=payload.priority.value,
            assignee_id=payload.assignee_id,
            project_id=payload.project_id,
            due_at=payload.due_at,
            tags=payload.tags,
            creator_id=user_id,
        )
        await self.repo.add_history(task.id, user_id, "create", after=payload.model_dump(exclude_none=True))
        return TaskDTO.model_validate(task, from_attributes=True)

    async def update_task(self, task_id: int, payload: TaskUpdate, user_id: int) -> TaskDTO:
        task = await self.repo.get(task_id)
        if not task or task.is_deleted:
            raise TaskNotFoundException()
        await self._check_write_access(task, user_id)
        old = TaskDTO.model_validate(task, from_attributes=True).model_dump()
        update_data = payload.model_dump(exclude_none=True)
        updated = await self.repo.update_task(task, **update_data)
        await self.repo.add_history(task_id, user_id, "update", before=old, after=update_data)
        return TaskDTO.model_validate(updated, from_attributes=True)

    async def delete_task(self, task_id: int, user_id: int) -> dict:
        task = await self.repo.get(task_id)
        if not task or task.is_deleted:
            raise TaskNotFoundException()
        await self._check_write_access(task, user_id)
        await self.repo.soft_delete(task_id)
        return {"deleted": True}

    async def batch_update_status(self, req: BatchUpdateStatusRequest, user_id: int) -> dict:
        if len(req.ids) > 10 and not req.action_id:
            raise PermissionDeniedException("批量操作超过10项，需先获取actionId确认")
        if req.action_id:
            await self.action_svc.verify_action(req.action_id, user_id, "batch_update_task_status")
        updated = await self.repo.batch_update_status(req.ids, req.status.value, user_id)
        return {"updated": updated}

    async def batch_assign(self, req: BatchAssignRequest, user_id: int) -> dict:
        updated = await self.repo.batch_assign(req.ids, req.assignee_id, user_id)
        return {"updated": updated}

    async def get_history(self, task_id: int, user_id: int) -> list[TaskHistoryDTO]:
        task = await self.repo.get(task_id)
        if not task:
            raise TaskNotFoundException()
        history = await self.repo.get_history(task_id)
        return [
            TaskHistoryDTO(
                id=h.id, task_id=h.task_id, user_id=h.user_id,
                user_name=h.user.name if h.user else "",
                op=h.op, before=h.before, after=h.after,
                gmt_create=h.gmt_create,
            )
            for h in history
        ]

    async def _check_read_access(self, task: Task, user_id: int):
        if task.creator_id == user_id or task.assignee_id == user_id:
            return
        if task.project_id and await self.repo.is_project_member(task.project_id, user_id):
            return
        raise PermissionDeniedException()

    async def _check_write_access(self, task: Task, user_id: int):
        if task.creator_id == user_id or task.assignee_id == user_id:
            return
        if task.project_id and await self.repo.is_project_owner(task.project_id, user_id):
            return
        raise PermissionDeniedException()
