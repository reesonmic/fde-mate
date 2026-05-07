"""
AI Orchestrator Exceptions Module

Provides:
- Error code constants (codes.py) - aligned with api layer 8xxx segment
- Business exception classes (biz.py)
- FastAPI exception handlers (handlers.py)

Usage:
    from app.exceptions.biz import AIInvalidParamsException
    raise AIInvalidParamsException("query too long")
"""
from app.exceptions.biz import (
    BizException,
    SystemException,
    AIInvalidParamsException,
    AIActionNotFoundException,
    AIActionExpiredException,
    AIRagSearchException,
    AISafetyBlockedException,
    AIInternalException,
)
from app.exceptions.handlers import setup_exception_handlers

__all__ = [
    "BizException",
    "SystemException",
    "AIInvalidParamsException",
    "AIActionNotFoundException",
    "AIActionExpiredException",
    "AIRagSearchException",
    "AISafetyBlockedException",
    "AIInternalException",
    "setup_exception_handlers",
]
