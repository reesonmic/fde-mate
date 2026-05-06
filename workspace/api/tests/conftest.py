"""Shared test fixtures and utilities."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_db_session():
    """Create a mock async database session."""
    session = AsyncMock(spec=AsyncSession)
    session.add = AsyncMock()
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.execute = AsyncMock()
    session.get = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def sample_user():
    from app.models.user import User
    return User(
        id=1,
        name="test_user",
        email="test@example.com",
        role="fde",
        level="P6",
    )


@pytest.fixture
def sample_task():
    from app.models.task import Task
    return Task(
        id=1,
        title="Test Task",
        description="A test task",
        status="todo",
        priority="p1",
        assignee_id=1,
        project_id=1,
        gmt_create=datetime.utcnow(),
        gmt_modified=datetime.utcnow(),
        is_deleted=0,
    )


@pytest.fixture
def sample_project():
    from app.models.project import Project
    return Project(
        id=1,
        name="Test Project",
        description="A test project",
        phase="init",
        health=80,
        owner_id=1,
        start_at=datetime.utcnow(),
        gmt_create=datetime.utcnow(),
        gmt_modified=datetime.utcnow(),
        is_deleted=0,
    )


@pytest.fixture
def sample_customer():
    from app.models.customer import Customer
    return Customer(
        id=1,
        name="Test Customer",
        industry="Technology",
        scale="large",
        gmt_create=datetime.utcnow(),
        gmt_modified=datetime.utcnow(),
        is_deleted=0,
    )


@pytest.fixture
def sample_coach():
    from app.models.coach import Coach
    return Coach(
        id=1,
        title="Test Best Practice",
        scenario="Deployment",
        summary="A test best practice",
        category="best_practice",
        gmt_create=datetime.utcnow(),
        gmt_modified=datetime.utcnow(),
        is_deleted=0,
    )


@pytest.fixture
def sample_file():
    from app.models.file import File
    return File(
        id=1,
        name="test.doc",
        ext="doc",
        size=1024,
        scope="project",
        scope_id=1,
        owner_id=1,
        rag_indexed=False,
        gmt_create=datetime.utcnow(),
        gmt_modified=datetime.utcnow(),
        is_deleted=0,
    )


@pytest.fixture
def sample_ai_message():
    from app.models.ai import AiMessage
    return AiMessage(
        id=1,
        session_id=1,
        role="user",
        content="Hello",
        gmt_create=datetime.utcnow(),
    )


@pytest.fixture
def sample_ai_session():
    from app.models.ai import AiSession
    return AiSession(
        id=1,
        user_id=1,
        assistant_key="chat",
        mode="smart",
        title="Test Session",
        gmt_create=datetime.utcnow(),
        gmt_modified=datetime.utcnow(),
    )
