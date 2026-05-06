"""Tests for AuthService."""
from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from app.services.auth_service import AuthService


class TestAuthLogin:
    """TC-AUTH-S-001: User login."""

    @pytest.mark.asyncio
    async def test_login_success(self, mock_db_session):
        """Login should return tokens for valid credentials."""
        user_repo = AsyncMock()
        user_repo.find_by_email_or_name.return_value = MagicMock(
            id=1,
            name="testuser",
            email="test@example.com",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIL9lqS.0q",
        )

        service = AuthService(mock_db_session, user_repo)
        result = await service.login(
            identifier="test@example.com",
            password="password123",
        )

        assert "access_token" in result
        assert "refresh_token" in result

    @pytest.mark.asyncio
    async def test_login_user_not_found_raises(self, mock_db_session):
        """Login should raise for non-existent user."""
        user_repo = AsyncMock()
        user_repo.find_by_email_or_name.return_value = None

        service = AuthService(mock_db_session, user_repo)

        with pytest.raises(Exception):
            await service.login(
                identifier="nonexistent",
                password="password123",
            )

    @pytest.mark.asyncio
    async def test_login_wrong_password_raises(self, mock_db_session):
        """Login should raise for wrong password."""
        user_repo = AsyncMock()
        user_repo.find_by_email_or_name.return_value = MagicMock(
            id=1,
            name="testuser",
            hashed_password="$2b$12$wronghash",
        )

        service = AuthService(mock_db_session, user_repo)

        with pytest.raises(Exception):
            await service.login(
                identifier="testuser",
                password="wrongpassword",
            )


class TestAuthRegister:
    """TC-AUTH-S-002: User registration."""

    @pytest.mark.asyncio
    async def test_register_success(self, mock_db_session):
        """Register should create new user."""
        user_repo = AsyncMock()
        user_repo.create.return_value = MagicMock(
            id=1, name="newuser", email="new@example.com",
        )

        service = AuthService(mock_db_session, user_repo)
        result = await service.register(
            name="newuser",
            email="new@example.com",
            password="password123",
        )

        assert result.name == "newuser"
        user_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_empty_email_raises(self, mock_db_session):
        """Register should reject empty email."""
        user_repo = AsyncMock()
        service = AuthService(mock_db_session, user_repo)

        with pytest.raises(ValueError):
            await service.register(
                name="newuser",
                email="",
                password="password123",
            )


class TestAuthRefresh:
    """TC-AUTH-S-003: Token refresh."""

    @pytest.mark.asyncio
    async def test_refresh_token_success(self, mock_db_session):
        """Refresh should return new access token."""
        service = AuthService(mock_db_session, AsyncMock())

        # Generate a refresh token first
        _, refresh_token = await service.login(
            identifier="test@example.com",
            password="password123",
        )

        # Mock user_repo for refresh
        service.user_repo.find_by_id = AsyncMock(return_value=MagicMock(id=1))

        result = await service.refresh(refresh_token)

        assert "access_token" in result

    @pytest.mark.asyncio
    async def test_refresh_token_invalid_raises(self, mock_db_session):
        """Refresh should raise for invalid token."""
        service = AuthService(mock_db_session, AsyncMock())

        with pytest.raises(Exception):
            await service.refresh("invalid-token")
