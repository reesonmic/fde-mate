"""
Action Service - 二次确认 stage/verify/execute/cancel.
"""
import json
import uuid
from datetime import datetime, timedelta

from redis.asyncio import Redis

from app.config.settings import settings
from app.exceptions.biz import (
    AIActionNotFoundException, AIActionExpiredException,
    AIActionUserMismatchException, AIActionToolMismatchException,
)


class ActionService:
    PREFIX = "action:"
    TTL_SECONDS = 60

    def __init__(self, redis_client: Redis | None = None):
        self.redis = redis_client
        self._memory_store: dict[str, dict] = {}  # Fallback if Redis not available

    async def stage(self, *, tool_name: str, args: dict, user_id: int,
                    title: str, severity: str, preview: dict,
                    affected_items: list | None = None) -> dict:
        action_id = str(uuid.uuid4())
        payload = {
            "tool_name": tool_name,
            "args": args,
            "user_id": user_id,
            "title": title,
            "severity": severity,
            "preview": preview,
            "affected_items": affected_items or [],
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
        }
        if self.redis:
            await self.redis.setex(
                f"{self.PREFIX}{action_id}",
                self.TTL_SECONDS,
                json.dumps(payload),
            )
        else:
            self._memory_store[action_id] = payload

        return {
            "action_id": action_id,
            "title": title,
            "severity": severity,
            "preview": preview,
            "affected_items": affected_items,
            "expires_at": (datetime.utcnow() + timedelta(seconds=self.TTL_SECONDS)).isoformat(),
        }

    async def verify_action(self, action_id: str, user_id: int, tool_name: str) -> dict:
        payload = await self._get_action(action_id)
        if not payload:
            raise AIActionNotFoundException()
        if payload.get("status") != "pending":
            raise AIActionExpiredException()
        if payload.get("user_id") != user_id:
            raise AIActionUserMismatchException()
        if payload.get("tool_name") != tool_name:
            raise AIActionToolMismatchException()
        return payload

    async def execute_action(self, action_id: str, user_id: int) -> dict:
        payload = await self._get_action(action_id)
        if not payload:
            raise AIActionNotFoundException()
        if payload.get("status") != "pending":
            raise AIActionExpiredException()
        if payload.get("user_id") != user_id:
            raise AIActionUserMismatchException()
        # Verify tool_name is non-empty
        if not payload.get("tool_name"):
            raise AIActionToolMismatchException()
        payload["status"] = "executed"
        await self._save_action(action_id, payload)
        return {"success": True, "result": payload.get("args", {})}

    async def cancel_action(self, action_id: str, user_id: int) -> dict:
        payload = await self._get_action(action_id)
        if not payload:
            raise AIActionNotFoundException()
        if payload.get("user_id") != user_id:
            raise AIActionUserMismatchException()
        payload["status"] = "cancelled"
        await self._save_action(action_id, payload)
        return {"cancelled": True}

    async def preview_action(self, tool_name: str, args: dict, user_id: int) -> dict:
        return await self.stage(
            tool_name=tool_name,
            args=args,
            user_id=user_id,
            title=f"执行 {tool_name}",
            severity="low",
            preview=args,
        )

    async def _get_action(self, action_id: str) -> dict | None:
        if self.redis:
            raw = await self.redis.get(f"{self.PREFIX}{action_id}")
            if raw:
                return json.loads(raw)
            return None
        return self._memory_store.get(action_id)

    async def _save_action(self, action_id: str, payload: dict):
        if self.redis:
            await self.redis.setex(
                f"{self.PREFIX}{action_id}",
                self.TTL_SECONDS,
                json.dumps(payload),
            )
        else:
            self._memory_store[action_id] = payload
