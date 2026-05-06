"""Tests for ProjectService."""
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.models.project import Project, ProjectMember
from app.services.project_service import ProjectService


class TestProjectServiceCreateProject:
    """TC-PROJ-S-001: Create project with valid data."""

    @pytest.mark.asyncio
    async def test_create_project_success(self, mock_db_session, sample_user):
        """Create project should succeed with valid data."""
        project_repo = AsyncMock()
        project_repo.create.return_value = Project(
            id=1,
            name="New Project",
            description="Project description",
            phase="init",
            health=100,
            owner_id=1,
            start_at=datetime.utcnow(),
            gmt_create=datetime.utcnow(),
            gmt_modified=datetime.utcnow(),
        )

        service = ProjectService(mock_db_session, project_repo)
        result = await service.create_project(
            name="New Project",
            description="Project description",
            owner_id=1,
            customer_id=None,
        )

        assert result.name == "New Project"
        project_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_project_empty_name_raises(self, mock_db_session):
        """Create project should reject empty name."""
        project_repo = AsyncMock()
        service = ProjectService(mock_db_session, project_repo)

        with pytest.raises(ValueError):
            await service.create_project(
                name="",
                description="desc",
                owner_id=1,
            )

    @pytest.mark.asyncio
    async def test_create_project_adds_owner_as_member(self, mock_db_session):
        """Create project should add owner as a member."""
        project_repo = AsyncMock()
        project_repo.create.return_value = Project(
            id=1,
            name="New Project",
            description="desc",
            phase="init",
            health=100,
            owner_id=1,
            start_at=datetime.utcnow(),
            gmt_create=datetime.utcnow(),
            gmt_modified=datetime.utcnow(),
        )

        service = ProjectService(mock_db_session, project_repo)
        await service.create_project(
            name="New Project",
            description="desc",
            owner_id=1,
        )

        project_repo.add_member.assert_called_once()


class TestProjectServiceListProjects:
    """TC-PROJ-S-002: List projects with pagination."""

    @pytest.mark.asyncio
    async def test_list_projects_success(self, mock_db_session):
        """List projects should return paginated results."""
        project_repo = AsyncMock()
        project_repo.list.return_value = (
            [Project(
                id=1, name="Project 1", phase="delivery", health=80,
                owner_id=1, start_at=datetime.utcnow(),
                gmt_create=datetime.utcnow(), gmt_modified=datetime.utcnow(),
            )],
            1,
        )

        service = ProjectService(mock_db_session, project_repo)
        projects, total = await service.list_projects(user_id=1)

        assert len(projects) == 1
        assert total == 1

    @pytest.mark.asyncio
    async def test_list_projects_with_phase_filter(self, mock_db_session):
        """List projects should filter by phase."""
        project_repo = AsyncMock()
        project_repo.list.return_value = ([], 0)

        service = ProjectService(mock_db_session, project_repo)
        tasks, total = await service.list_projects(
            user_id=1, phase="delivery"
        )

        call_kwargs = project_repo.list.call_args[1]
        assert call_kwargs["phase"] == "delivery"


class TestProjectServiceUpdateProject:
    """TC-PROJ-S-003: Update project."""

    @pytest.mark.asyncio
    async def test_update_project_success(self, mock_db_session):
        """Update project should succeed."""
        project_repo = AsyncMock()
        project_repo.get.return_value = Project(
            id=1, name="Old Name", phase="init", health=80,
            owner_id=1, start_at=datetime.utcnow(),
            gmt_create=datetime.utcnow(), gmt_modified=datetime.utcnow(),
        )

        service = ProjectService(mock_db_session, project_repo)
        result = await service.update_project(
            project_id=1, name="New Name", user_id=1
        )

        assert result.name == "New Name"
        project_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_project_not_found_raises(self, mock_db_session):
        """Update project should raise for non-existent project."""
        project_repo = AsyncMock()
        project_repo.get.return_value = None

        service = ProjectService(mock_db_session, project_repo)

        with pytest.raises(Exception):
            await service.update_project(
                project_id=999, name="New Name", user_id=1
            )


class TestProjectServiceDeleteProject:
    """TC-PROJ-S-004: Soft delete project."""

    @pytest.mark.asyncio
    async def test_delete_project_success(self, mock_db_session):
        """Delete project should soft-delete."""
        project_repo = AsyncMock()
        project_repo.get.return_value = Project(
            id=1, name="Project", phase="init", health=80,
            owner_id=1, start_at=datetime.utcnow(),
            gmt_create=datetime.utcnow(), gmt_modified=datetime.utcnow(),
        )

        service = ProjectService(mock_db_session, project_repo)
        await service.delete_project(project_id=1, user_id=1)

        project_repo.soft_delete.assert_called_once()
