"""Tests for TaskService."""
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.task import Task
from app.schemas.task import TaskDTO
from app.services.task_service import TaskService


class TestTaskServiceCreateTask:
    """TC-TASK-S-001: Create task with valid data."""

    @pytest.mark.asyncio
    async def test_create_task_success(self, mock_db_session, sample_user):
        """Create task should succeed with valid data."""
        task_repo = AsyncMock()
        task_repo.create.return_value = Task(
            id=1,
            title="New Task",
            description="Task description",
            status="todo",
            priority="p2",
            assignee_id=1,
            gmt_create=datetime.utcnow(),
            gmt_modified=datetime.utcnow(),
        )

        service = TaskService(mock_db_session, task_repo)
        result = await service.create_task(
            title="New Task",
            description="Task description",
            assignee_id=1,
            priority="p2",
            project_id=1,
        )

        assert result.title == "New Task"
        task_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_task_empty_title_raises(self, mock_db_session):
        """Create task should reject empty title."""
        task_repo = AsyncMock()
        service = TaskService(mock_db_session, task_repo)

        with pytest.raises(ValueError):
            await service.create_task(
                title="",
                description="desc",
            )

    @pytest.mark.asyncio
    async def test_create_task_title_too_long_raises(self, mock_db_session):
        """Create task should reject title > 255 chars."""
        task_repo = AsyncMock()
        service = TaskService(mock_db_session, task_repo)

        with pytest.raises(ValueError):
            await service.create_task(
                title="x" * 256,
                description="desc",
            )


class TestTaskServiceListTasks:
    """TC-TASK-S-002: List tasks with pagination and filters."""

    @pytest.mark.asyncio
    async def test_list_tasks_no_filters(self, mock_db_session):
        """List tasks should return all tasks."""
        task_repo = AsyncMock()
        task_repo.list.return_value = (
            [Task(
                id=1, title="Task 1", status="todo", priority="p1",
                gmt_create=datetime.utcnow(), gmt_modified=datetime.utcnow(),
            )],
            1,
        )

        service = TaskService(mock_db_session, task_repo)
        tasks, total = await service.list_tasks(user_id=1)

        assert len(tasks) == 1
        assert total == 1
        task_repo.list.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_tasks_with_status_filter(self, mock_db_session):
        """List tasks should filter by status."""
        task_repo = AsyncMock()
        task_repo.list.return_value = ([], 0)

        service = TaskService(mock_db_session, task_repo)
        tasks, total = await service.list_tasks(
            user_id=1, status="in_progress"
        )

        assert total == 0
        task_repo.list.assert_called_once()
        call_kwargs = task_repo.list.call_args[1]
        assert call_kwargs["status"] == "in_progress"

    @pytest.mark.asyncio
    async def test_list_tasks_with_keyword(self, mock_db_session):
        """List tasks should filter by keyword."""
        task_repo = AsyncMock()
        task_repo.list.return_value = ([], 0)

        service = TaskService(mock_db_session, task_repo)
        tasks, total = await service.list_tasks(
            user_id=1, keyword="test"
        )

        call_kwargs = task_repo.list.call_args[1]
        assert call_kwargs["keyword"] == "test"


class TestTaskServiceUpdateTaskStatus:
    """TC-TASK-S-003: Update task status."""

    @pytest.mark.asyncio
    async def test_update_task_status_success(self, mock_db_session, sample_task):
        """Update task status should succeed."""
        task_repo = AsyncMock()
        task_repo.get.return_value = sample_task

        service = TaskService(mock_db_session, task_repo)
        result = await service.update_task_status(
            task_id=1, status="in_progress", user_id=1
        )

        assert result.status == "in_progress"
        task_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_task_status_not_found_raises(self, mock_db_session):
        """Update task status should raise for non-existent task."""
        task_repo = AsyncMock()
        task_repo.get.return_value = None

        service = TaskService(mock_db_session, task_repo)

        with pytest.raises(Exception):
            await service.update_task_status(
                task_id=999, status="done", user_id=1
            )

    @pytest.mark.asyncio
    async def test_update_task_status_invalid_status_raises(self, mock_db_session, sample_task):
        """Update task status should reject invalid status."""
        task_repo = AsyncMock()
        task_repo.get.return_value = sample_task

        service = TaskService(mock_db_session, task_repo)

        with pytest.raises(ValueError):
            await service.update_task_status(
                task_id=1, status="invalid", user_id=1
            )


class TestTaskServiceBatchUpdateStatus:
    """TC-TASK-S-004: Batch update task status."""

    @pytest.mark.asyncio
    async def test_batch_update_success(self, mock_db_session):
        """Batch update should update multiple tasks."""
        task_repo = AsyncMock()
        task_repo.batch_update.return_value = 3

        service = TaskService(mock_db_session, task_repo)
        count = await service.batch_update_status(
            task_ids=[1, 2, 3], status="done", user_id=1
        )

        assert count == 3
        task_repo.batch_update.assert_called_once()

    @pytest.mark.asyncio
    async def test_batch_update_empty_ids_raises(self, mock_db_session):
        """Batch update should reject empty task list."""
        task_repo = AsyncMock()
        service = TaskService(mock_db_session, task_repo)

        with pytest.raises(ValueError):
            await service.batch_update_status(
                task_ids=[], status="done", user_id=1
            )


class TestTaskServiceDeleteTask:
    """TC-TASK-S-005: Soft delete task."""

    @pytest.mark.asyncio
    async def test_delete_task_success(self, mock_db_session, sample_task):
        """Delete task should soft-delete."""
        task_repo = AsyncMock()
        task_repo.get.return_value = sample_task

        service = TaskService(mock_db_session, task_repo)
        await service.delete_task(task_id=1, user_id=1)

        task_repo.soft_delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_task_not_found_raises(self, mock_db_session):
        """Delete task should raise for non-existent task."""
        task_repo = AsyncMock()
        task_repo.get.return_value = None

        service = TaskService(mock_db_session, task_repo)

        with pytest.raises(Exception):
            await service.delete_task(task_id=999, user_id=1)
