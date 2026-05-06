"""
Exception Handlers for FastAPI
"""
import uuid
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.biz import BizException, SystemException
from app.exceptions.codes import BIZ_INVALID_PARAMS
from app.config.logging import get_logger

logger = get_logger("exception")


def _get_trace_id(request: Request) -> str:
    return getattr(request.state, "trace_id", None) or str(uuid.uuid4())[:8]


def _error_response(code: int, message: str, details=None, trace_id: str = None, data=None) -> dict:
    return {
        "code": code,
        "message": message,
        "data": data,
        "traceId": trace_id,
        **({"details": details} if details is not None else {}),
    }


def setup_exception_handlers(app):
    """Setup exception handlers for the FastAPI app."""

    @app.exception_handler(BizException)
    async def biz_exception_handler(request: Request, exc: BizException):
        trace_id = _get_trace_id(request)
        logger.error("biz_exception", code=exc.code, message=exc.message, details=exc.details, trace_id=trace_id)
        return JSONResponse(
            status_code=exc.http_status,
            content=_error_response(
                code=exc.code,
                message=exc.message,
                details=exc.details,
                trace_id=trace_id,
            ),
        )

    @app.exception_handler(SystemException)
    async def system_exception_handler(request: Request, exc: SystemException):
        trace_id = _get_trace_id(request)
        logger.error("system_exception", code=exc.code, message=exc.message, details=exc.details, trace_id=trace_id)
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
        logger.error("http_exception", status_code=exc.status_code, detail=exc.detail, trace_id=trace_id)
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_response(
                code=exc.status_code,
                message=exc.detail,
                trace_id=trace_id,
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        trace_id = _get_trace_id(request)
        logger.error("validation_error", errors=exc.errors(), trace_id=trace_id)
        return JSONResponse(
            status_code=400,
            content=_error_response(
                code=BIZ_INVALID_PARAMS,
                message="Invalid request parameters",
                details=exc.errors(),
                trace_id=trace_id,
            ),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        trace_id = _get_trace_id(request)
        logger.exception("unhandled_exception", error=str(exc), trace_id=trace_id)
        return JSONResponse(
            status_code=500,
            content=_error_response(
                code=9001,
                message="Internal server error",
                trace_id=trace_id,
            ),
        )