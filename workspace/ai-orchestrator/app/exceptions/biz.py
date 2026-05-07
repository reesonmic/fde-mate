"""
AI Orchestrator Business Exception Classes
"""
from typing import Optional, Any

from app.exceptions.codes import (
    BIZ_INVALID_PARAMS,
    BIZ_AI_ACTION_NOT_FOUND,
    BIZ_AI_ACTION_EXPIRED,
    BIZ_AI_PROMPT_INJECTION,
    BIZ_AI_RAG_SEARCH_FAILED,
    SYS_INTERNAL_ERROR,
)


class BizException(Exception):
    """Base business exception for ai-orchestrator."""

    def __init__(
        self,
        code: int,
        message: str,
        details: Optional[Any] = None,
        http_status: Optional[int] = None,
    ):
        self.code = code
        self.message = message
        self.details = details
        self._http_status = http_status
        super().__init__(message)

    @property
    def http_status(self) -> int:
        if self._http_status is not None:
            return self._http_status
        if self.code >= 9000:
            return 500
        if self.code in (BIZ_AI_ACTION_NOT_FOUND,):
            return 404
        return 400


class SystemException(Exception):
    """Base system exception for ai-orchestrator."""

    def __init__(
        self,
        code: int,
        message: str,
        details: Optional[Any] = None,
    ):
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)

    @property
    def http_status(self) -> int:
        return 500


class AIInvalidParamsException(BizException):
    """Invalid parameters."""

    def __init__(self, message: str = "Invalid parameters", details: Optional[Any] = None):
        super().__init__(BIZ_INVALID_PARAMS, message, details=details, http_status=400)


class AIActionNotFoundException(BizException):
    """Action not found in Redis cache."""

    def __init__(self):
        super().__init__(BIZ_AI_ACTION_NOT_FOUND, "Action not found", http_status=404)


class AIActionExpiredException(BizException):
    """Action expired (60s TTL)."""

    def __init__(self):
        super().__init__(BIZ_AI_ACTION_EXPIRED, "Action expired (60s TTL)", http_status=410)


class AISafetyBlockedException(BizException):
    """Input blocked by safety guard."""

    def __init__(self, reason: str):
        super().__init__(
            BIZ_AI_PROMPT_INJECTION,
            f"Request blocked by safety guard: {reason}",
            http_status=400,
        )


class AIRagSearchException(BizException):
    """RAG search failed."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(BIZ_AI_RAG_SEARCH_FAILED, message, details=details, http_status=500)


class AIInternalException(SystemException):
    """Generic internal error."""

    def __init__(self, message: str = "AI service internal error", details: Optional[Any] = None):
        super().__init__(SYS_INTERNAL_ERROR, message, details=details)
