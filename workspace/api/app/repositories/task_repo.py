"""
Task Repository.
"""
from sqlalchemy import select, func, or_, update
from app.models.task import Task, TaskHistory
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    model = Task

    async def search(self, keyword: str | None = None, status: list[str] | None = None,
                     assignee_id: int | None = None, project_id: int | None = None,
                     priority: list[str] | None = None, viewer_id: int | None = None,
                     page: int = 1, size: int = 20) -> tuple[list[Task], int]:
        stmt = select(Task).where(Task.is_deleted == 0)

        if viewer_id:
            stmt = stmt.where(
                or_(Task.creator_id == viewer_id, Task.assignee_id == viewer_id)
            )
        if keyword:
            stmt = stmt.where(Task.title.contains(keyword))
        if status:
            stmt = stmt.where(Task.status.in_(status))
        if assignee_id:
            stmt = stmt.where(Task.assignee_id == assignee_id)
        if project_id:
            stmt = stmt.where(Task.project_id == project_id)
        if priority:
            stmt = stmt.where(Task.priority.in_(priority))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.session.scalar(count_stmt) or 0

        stmt = stmt.order_by(Task.gmt_create.desc())
        stmt = stmt.offset((page - 1) * size).limit(size)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def create_task(self, **kwargs) -> Task:
        task = Task(**kwargs)
        self.session.add(task)
        await self.session.flush()
        return task

    async def update_task(self, task: Task, **kwargs) -> Task:
        for k, v in kwargs.items():
            if v is not None:
                setattr(task, k, v)
        await self.session.flush()
        return task

    async def batch_update_status(self, ids: list[int], status: str, viewer_id: int) -> int:
        stmt = (
            update(Task)
            .where(
                Task.id.in_(ids),
                or_(Task.creator_id == viewer_id, Task.assignee_id == viewer_id),
            )
            .values(status=status)
        )
        result = await self.session.execute(stmt)
        return result.rowcount or 0

    async def batch_assign(self, ids: list[int], assignee_id: int, viewer_id: int) -> int:
        stmt = (
            update(Task)
            .where(
                Task.id.in_(ids),
                or_(Task.creator_id == viewer_id, Task.assignee_id == viewer_id),
            )
            .values(assignee_id=assignee_id)
        )
        result = await self.session.execute(stmt)
        return result.rowcount or 0

    async def add_history(self, task_id: int, user_id: int, op: str, before: dict | None = None, after: dict | None = None):
        history = TaskHistory(task_id=task_id, user_id=user_id, op=op, before=before, after=after)
        self.session.add(history)

    async def get_history(self, task_id: int) -> list[TaskHistory]:
        result = await self.session.execute(
            select(TaskHistory).where(TaskHistory.task_id == task_id).order_by(TaskHistory.gmt_create.desc())
        )
        return list(result.scalars().all())

    async def is_project_member(self, project_id: int, user_id: int) -> bool:
        from app.models.project import ProjectMember
        result = await self.session.execute(
            select(func.count()).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
            )
        )
        return (result.scalar() or 0) > 0

    async def is_project_owner(self, project_id: int, user_id: int) -> bool:
        from app.models.project import Project
        project = await self.session.get(Project, project_id)
        return project is not None and project.owner_id == user_id

    # ---------- Dashboard helpers (M6-API-07) ----------

    async def count_by_assignee(self, assignee_id: int) -> int:
        return await self.session.scalar(
            select(func.count()).where(
                Task.is_deleted == 0, Task.assignee_id == assignee_id
            )
        ) or 0

    async def count_pending_by_assignee(self, assignee_id: int) -> int:
        """统计待处理任务数量（状态为todo或in_progress）"""
        return await self.session.scalar(
            select(func.count()).where(
                Task.is_deleted == 0,
                Task.assignee_id == assignee_id,
                Task.status.in_(["todo", "in_progress", "blocked"])
            )
        ) or 0

    async def list_recent_by_assignee(self, assignee_id: int, limit: int) -> list[Task]:
        result = await self.session.execute(
            select(Task)
            .where(Task.is_deleted == 0, Task.assignee_id == assignee_id)
            .order_by(Task.gmt_create.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def list_created_since(self, assignee_id: int, since, limit: int = 20) -> list[Task]:
        result = await self.session.execute(
            select(Task)
            .where(
                Task.is_deleted == 0,
                Task.assignee_id == assignee_id,
                Task.gmt_create >= since,
            )
            .order_by(Task.gmt_create.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
