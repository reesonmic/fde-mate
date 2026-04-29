"""
Business Exception Classes
"""
from typing import Optional, Any

from app.exceptions.codes import *


class BizException(Exception):
    """Base business exception."""

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
        """Get HTTP status code based on error code."""
        if self.code >= 9000:
            return 500
        return 400


class AuthException(BizException):
    """Authentication exception."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(BIZ_AUTH_FAILED, message)


class TokenExpiredException(BizException):
    """Token expired exception."""

    def __init__(self, message: str = "Token expired"):
        super().__init__(BIZ_TOKEN_EXPIRED, message)


class TokenInvalidException(BizException):
    """Token invalid exception."""

    def __init__(self, message: str = "Token invalid"):
        super().__init__(BIZ_TOKEN_INVALID, message)


class PermissionDeniedException(BizException):
    """Permission denied exception."""

    def __init__(self, message: str = "Permission denied"):
        super().__init__(BIZ_PERMISSION_DENIED, message, http_status=403)


class NotFoundException(BizException):
    """Resource not found exception."""

    def __init__(self, resource: str, message: str = None):
        msg = message or f"{resource} not found"
        super().__init__(BIZ_NOT_FOUND, msg)


class TaskNotFoundException(NotFoundException):
    """Task not found exception."""

    def __init__(self):
        super().__init__("Task")


class ProjectNotFoundException(NotFoundException):
    """Project not found exception."""

    def __init__(self):
        super().__init__("Project")


class CustomerNotFoundException(NotFoundException):
    """Customer not found exception."""

    def __init__(self):
        super().__init__("Customer")


class FileNotFoundException(NotFoundException):
    """File not found exception."""

    def __init__(self):
        super().__init__("File")


class AIActionNotFoundException(BizException):
    """AI action not found exception."""

    def __init__(self):
        super().__init__(BIZ_AI_ACTION_NOT_FOUND, "Action not found")


class AIActionExpiredException(BizException):
    """AI action expired exception."""

    def __init__(self):
        super().__init__(BIZ_AI_ACTION_EXPIRED, "Action expired (60s TTL)")


class AIActionUserMismatchException(BizException):
    """AI action user mismatch exception."""

    def __init__(self):
        super().__init__(BIZ_AI_ACTION_USER_MISMATCH, "Action user mismatch")


class AIActionToolMismatchException(BizException):
    """AI action tool mismatch exception."""

    def __init__(self):
        super().__init__(BIZ_AI_ACTION_TOOL_MISMATCH, "Action tool mismatch")


class AIActionCancelledException(BizException):
    """AI action cancelled exception."""

    def __init__(self):
        super().__init__(BIZ_AI_ACTION_CANCELLED, "Action cancelled")


class SystemException(Exception):
    """Base system exception."""

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