"""Integration test fixtures and utilities."""
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


@pytest.fixture
def app_for_tests():
    """Create a FastAPI app with mocked dependencies for integration testing."""
    import os
    # Override settings for testing
    os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-testing-purposes-only"

    from app.main import app
    yield app


@pytest.fixture
async def mock_db():
    """Mock database session for integration tests."""
    session = AsyncMock(spec=AsyncSession)
    session.add = AsyncMock()
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.execute = AsyncMock()
    session.get = AsyncMock()
    session.delete = AsyncMock()
    session.scalar = AsyncMock()
    return session


@pytest.fixture
async def client(app_for_tests, mock_db):
    """Test client with mocked database."""
    with patch("app.deps.db.get_async_session", return_value=mock_db):
        transport = ASGITransport(app=app_for_tests)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


@pytest.fixture
def sample_user_model():
    """Sample User model instance."""
    from app.models.user import User
    return User(
        id=1,
        name="test_user",
        email="test@example.com",
        role="fde",
        level="P6",
    )


@pytest.fixture
def sample_task_model():
    """Sample Task model instance."""
    from app.models.task import Task
    task = Task(
        id=1,
        title="Integration Test Task",
        description="A test task for integration testing",
        status="todo",
        priority="p1",
        assignee_id=1,
        project_id=1,
        gmt_create=datetime.utcnow(),
        gmt_modified=datetime.utcnow(),
        is_deleted=0,
    )
    return task


@pytest.fixture
def sample_project_model():
    """Sample Project model instance."""
    from app.models.project import Project
    return Project(
        id=1,
        name="Integration Test Project",
        description="A test project for integration testing",
        phase="init",
        health=80,
        owner_id=1,
        start_at=datetime.utcnow(),
        gmt_create=datetime.utcnow(),
        gmt_modified=datetime.utcnow(),
        is_deleted=0,
    )


@pytest.fixture
def sample_customer_model():
    """Sample Customer model instance."""
    from app.models.customer import Customer
    return Customer(
        id=1,
        name="Integration Test Customer",
        industry="Technology",
        scale="large",
        gmt_create=datetime.utcnow(),
        gmt_modified=datetime.utcnow(),
        is_deleted=0,
    )
