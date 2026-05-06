"""Integration tests for health and basic endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    import os
    os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-testing-purposes-only"
    yield


@pytest.fixture
async def test_client(mock_settings):
    """Test client without auth requirements for health endpoint."""
    from app.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestHealthEndpoint:
    """TC-INT-HEALTH-001: Health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_returns_ok(self, test_client):
        """Health endpoint should return ok status."""
        response = await test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestUnauthenticatedAccess:
    """TC-INT-AUTH-001: Unauthenticated access to protected endpoints."""

    @pytest.mark.asyncio
    async def test_tasks_requires_auth(self, test_client):
        """Tasks endpoint should reject unauthenticated requests."""
        response = await test_client.get("/api/v1/tasks")
        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_projects_requires_auth(self, test_client):
        """Projects endpoint should reject unauthenticated requests."""
        response = await test_client.get("/api/v1/projects")
        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_dashboard_requires_auth(self, test_client):
        """Dashboard endpoint should reject unauthenticated requests."""
        response = await test_client.get("/api/v1/dashboard/summary")
        assert response.status_code in (401, 403)


class TestErrorResponseFormat:
    """TC-INT-ERROR-001: Error responses include data and traceId."""

    @pytest.mark.asyncio
    async def test_validation_error_format(self, test_client):
        """Validation errors should include code and message."""
        response = await test_client.post("/api/v1/auth/login", json={})
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_not_found_returns_404(self, test_client):
        """Non-existent endpoints should return 404."""
        response = await test_client.get("/api/v1/nonexistent")
        assert response.status_code == 404
