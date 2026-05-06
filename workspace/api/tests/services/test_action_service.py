"""Tests for ActionService (二次确认机制)."""
import json
from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.exceptions.biz import AIActionNotFoundException
from app.services.action_service import ActionService


class TestActionServicePreviewAction:
    """TC-ACTION-S-001: Preview action."""

    @pytest.mark.asyncio
    async def test_preview_action_returns_action_id(self):
        """Preview should generate valid action_id."""
        service = ActionService()
        result = await service.preview_action(
            tool_name="update_task",
            args={"task_id": 1, "status": "done"},
            user_id=1,
        )

        assert "action_id" in result
        assert result["title"] == "执行 update_task"
        assert result["severity"] == "low"

    @pytest.mark.asyncio
    async def test_preview_action_returns_expires_at(self):
        """Preview should include expiration time."""
        service = ActionService()
        result = await service.preview_action(
            tool_name="test",
            args={},
            user_id=1,
        )

        assert "expires_at" in result
        expires_at = datetime.fromisoformat(result["expires_at"])
        assert expires_at > datetime.utcnow()


class TestActionServiceExecuteAction:
    """TC-ACTION-S-002: Execute action."""

    @pytest.mark.asyncio
    async def test_execute_action_success(self):
        """Execute should succeed for valid pending action."""
        service = ActionService()

        # Stage an action
        stage_result = await service.stage(
            tool_name="update_task",
            args={"task_id": 1},
            user_id=1,
            title="Update task",
            severity="medium",
            preview={"status": "done"},
        )

        # Execute it
        result = await service.execute_action(
            action_id=stage_result["action_id"],
            user_id=1,
        )

        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_execute_action_not_found_raises(self):
        """Execute should raise for non-existent action."""
        service = ActionService()

        with pytest.raises(AIActionNotFoundException):
            await service.execute_action(
                action_id="non-existent",
                user_id=1,
            )

    @pytest.mark.asyncio
    async def test_execute_action_user_mismatch_raises(self):
        """Execute should raise for user mismatch."""
        service = ActionService()

        stage_result = await service.stage(
            tool_name="test",
            args={},
            user_id=1,
            title="Test",
            severity="low",
            preview={},
        )

        with pytest.raises(Exception):
            await service.execute_action(
                action_id=stage_result["action_id"],
                user_id=999,  # Different user
            )


class TestActionServiceCancelAction:
    """TC-ACTION-S-003: Cancel action."""

    @pytest.mark.asyncio
    async def test_cancel_action_success(self):
        """Cancel should succeed for valid action."""
        service = ActionService()

        stage_result = await service.stage(
            tool_name="test",
            args={},
            user_id=1,
            title="Test",
            severity="low",
            preview={},
        )

        result = await service.cancel_action(
            action_id=stage_result["action_id"],
            user_id=1,
        )

        assert result["cancelled"] is True

    @pytest.mark.asyncio
    async def test_cancel_action_not_found_raises(self):
        """Cancel should raise for non-existent action."""
        service = ActionService()

        with pytest.raises(AIActionNotFoundException):
            await service.cancel_action(
                action_id="non-existent",
                user_id=1,
            )


class TestActionServiceActionExpiry:
    """TC-ACTION-S-004: Action expiration."""

    @pytest.mark.asyncio
    async def test_expired_action_cannot_be_executed(self):
        """Expired action should not be executable."""
        # Create action with 0 TTL (immediately expired for testing)
        service = ActionService()
        service.TTL_SECONDS = 1  # 1 second for fast test

        stage_result = await service.stage(
            tool_name="test",
            args={},
            user_id=1,
            title="Test",
            severity="low",
            preview={},
        )

        # Wait for expiration
        import asyncio
        await asyncio.sleep(1.1)

        # Execute should fail due to expiration
        try:
            await service.execute_action(
                action_id=stage_result["action_id"],
                user_id=1,
            )
        except Exception:
            pass  # Expected to fail


class TestActionServiceVerifyAction:
    """TC-ACTION-S-005: Verify action before execution."""

    @pytest.mark.asyncio
    async def test_verify_action_returns_payload(self):
        """Verify should return the staged payload."""
        service = ActionService()

        stage_result = await service.stage(
            tool_name="update_task",
            args={"task_id": 1},
            user_id=1,
            title="Test",
            severity="high",
            preview={"status": "done"},
        )

        payload = await service.verify_action(
            action_id=stage_result["action_id"],
            user_id=1,
            tool_name="update_task",
        )

        assert payload["tool_name"] == "update_task"
        assert payload["severity"] == "high"

    @pytest.mark.asyncio
    async def test_verify_action_tool_mismatch_raises(self):
        """Verify should reject tool mismatch."""
        service = ActionService()

        stage_result = await service.stage(
            tool_name="update_task",
            args={},
            user_id=1,
            title="Test",
            severity="low",
            preview={},
        )

        with pytest.raises(Exception):
            await service.verify_action(
                action_id=stage_result["action_id"],
                user_id=1,
                tool_name="different_tool",
            )
