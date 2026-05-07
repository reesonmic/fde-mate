"""
FastAPI Exception Handlers for AI Orchestrator

Aligned with api layer response shape so the api layer can transparently
forward ai-orch errors to the web client without re-wrapping.

Response shape:
    {
        "code": <int error code>,
        "message": <str>,
        "data": null,
        "traceId": <str>,
        "details": <optional>
    }
"""
import logging
import uuid
from typing import Any, Optional

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.biz import BizException, SystemException
from app.exceptions.codes import BIZ_INVALID_PARAMS, SYS_INTERNAL_ERROR

logger = logging.getLogger("ai-orch.exception")


def _get_trace_id(request: Request) -> str:
    """Extract trace id from request state or X-Trace-Id header, or generate one."""
    state_trace = getattr(request.state, "trace_id", None)
    if state_trace:
        return state_trace
    header_trace = request.headers.get("X-Trace-Id")
    if header_trace:
        return header_trace
    return uuid.uuid4().hex[:8]


def _error_response(
    code: int,
    message: str,
    trace_id: str,
    details: Optional[Any] = None,
    data: Any = None,
) -> dict:
    body = {
        "code": code,
        "message": message,
        "data": data,
        "traceId": trace_id,
    }
    if details is not None:
        body["details"] = details
    return body


def setup_exception_handlers(app) -> None:
    """Register all exception handlers on the FastAPI app."""

    @app.exception_handler(BizException)
    async def biz_exception_handler(request: Request, exc: BizException):
        trace_id = _get_trace_id(request)
        logger.warning(
            "biz_exception code=%s message=%s trace_id=%s",
            exc.code, exc.message, trace_id,
        )
        return JSONResponse(
            status_code=exc.http_status,
            content=_error_response(
                code=exc.code,
                message=exc.message,
                trace_id=trace_id,
                details=exc.details,
            ),
        )

    @app.exception_handler(SystemException)
    async def system_exception_handler(request: Request, exc: SystemException):
        trace_id = _get_trace_id(request)
        logger.error(
            "system_exception code=%s message=%s trace_id=%s",
            exc.code, exc.message, trace_id,
        )
        return JSONResponse(
            status_code=500,
            content=_error_response(
                code=exc.code,
                message=exc.message,
                trace_id=trace_id,
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        trace_id = _get_trace_id(request)
        logger.warning(
            "http_exception status=%s detail=%s trace_id=%s",
            exc.status_code, exc.detail, trace_id,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_response(
                code=exc.status_code,
                message=str(exc.detail),
                trace_id=trace_id,
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        trace_id = _get_trace_id(request)
        logger.warning("validation_error trace_id=%s", trace_id)
        return JSONResponse(
            status_code=400,
            content=_error_response(
                code=BIZ_INVALID_PARAMS,
                message="Invalid request parameters",
                trace_id=trace_id,
                details=exc.errors(),
            ),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        trace_id = _get_trace_id(request)
        logger.exception("unhandled_exception trace_id=%s", trace_id)
        return JSONResponse(
            status_code=500,
            content=_error_response(
                code=SYS_INTERNAL_ERROR,
                message="Internal server error",
                trace_id=trace_id,
            ),
        )
