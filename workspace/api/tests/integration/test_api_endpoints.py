"""Integration tests for Task API endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime


@pytest.fixture
def app_with_mocks():
    """Create app with mocked DB and auth."""
    import os
    os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-testing-purposes-only"
    from app.main import app
    yield app


@pytest.fixture
def auth_user():
    """Mock UserContext for authenticated requests."""
    from app.deps.auth import UserContext
    return UserContext(
        id=1, name="test_user", email="test@example.com",
        roles=["fde"], level="P6",
    )


@pytest.fixture
async def api_client(app_with_mocks, auth_user):
    """Test client with mocked DB and auth."""
    from app.deps.db import get_async_session
    from app.deps.auth import current_user

    mock_session = AsyncMock()
    mock_session.add = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.execute = AsyncMock()
    mock_session.scalar = AsyncMock()

    # Override dependencies
    app = app_with_mocks
    app.dependency_overrides[get_async_session] = lambda: mock_session
    app.dependency_overrides[current_user] = lambda: auth_user

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac, mock_session

    app.dependency_overrides.clear()


class TestTaskListAPI:
    """TC-INT-TASK-LIST-001: List tasks endpoint."""

    @pytest.mark.asyncio
    async def test_list_tasks_returns_list(self, api_client):
        """List tasks should return paginated results."""
        client, mock_session = api_client
        mock_result = MagicMock()
        mock_result.items = []
        mock_result.total = 0
        mock_session.execute.return_value = mock_result

        response = await client.get("/api/v1/tasks")
        assert response.status_code == 200


class TestTaskCreateAPI:
    """TC-INT-TASK-CREATE-001: Create task endpoint."""

    @pytest.mark.asyncio
    async def test_create_task_with_valid_data(self, api_client):
        """Create task should accept valid data."""
        client, mock_session = api_client
        mock_session.execute.return_value = MagicMock(scalar_one_or_none=MagicMock())

        response = await client.post("/api/v1/tasks", json={
            "title": "New Task",
            "description": "Test task",
            "priority": "p1",
            "status": "todo",
            "project_id": 1,
        })
        assert response.status_code in (200, 201)

    @pytest.mark.asyncio
    async def test_create_task_rejects_missing_title(self, api_client):
        """Create task should reject requests without title."""
        client, _ = api_client
        response = await client.post("/api/v1/tasks", json={
            "description": "Missing title",
        })
        assert response.status_code in (400, 422)


class TestTaskUpdateAPI:
    """TC-INT-TASK-UPDATE-001: Update task endpoint."""

    @pytest.mark.asyncio
    async def test_update_task_status(self, api_client):
        """Update task should accept status changes."""
        client, mock_session = api_client
        mock_session.execute.return_value = MagicMock(scalar_one_or_none=MagicMock(
            id=1, title="Task", status="todo", priority="p1", project_id=1,
            gmt_create=datetime.utcnow(), gmt_modified=datetime.utcnow(),
            is_deleted=0, assignee_id=1, description="", deadline=None,
            creator_id=1,
        ))

        response = await client.put("/api/v1/tasks/1", json={
            "status": "done",
        })
        assert response.status_code == 200


class TestDashboardAPI:
    """TC-INT-DASH-001: Dashboard endpoints."""

    @pytest.mark.asyncio
    async def test_dashboard_summary(self, api_client):
        """Dashboard summary should return counts."""
        client, mock_session = api_client
        mock_session.scalar.return_value = 0

        response = await client.get("/api/v1/dashboard/summary")
        assert response.status_code == 200
        data = response.json()
        assert "task_count" in data
        assert "project_count" in data
        assert "customer_count" in data


class TestMentionsAPI:
    """TC-INT-MENTION-001: Mentions search endpoint."""

    @pytest.mark.asyncio
    async def test_search_mentions(self, api_client):
        """Search mentions should return results."""
        client, mock_session = api_client
        mock_session.execute.return_value = MagicMock(scalars=MagicMock(all=MagicMock(return_value=[])))

        response = await client.get("/api/v1/mentions/search", params={"q": "test"})
        assert response.status_code == 200
