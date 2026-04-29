"""
Exception Handlers for FastAPI
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.biz import BizException, SystemException
from app.exceptions.codes import BIZ_INVALID_PARAMS
from app.config.logging import get_logger

logger = get_logger("exception")


def setup_exception_handlers(app):
    """Setup exception handlers for the FastAPI app."""

    @app.exception_handler(BizException)
    async def biz_exception_handler(request: Request, exc: BizException):
        logger.error("biz_exception", code=exc.code, message=exc.message, details=exc.details)
        return JSONResponse(
            status_code=exc.http_status,
            content={
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(SystemException)
    async def system_exception_handler(request: Request, exc: SystemException):
        logger.error("system_exception", code=exc.code, message=exc.message, details=exc.details)
        return JSONResponse(
            status_code=500,
            content={
                "code": exc.code,
                "message": exc.message,
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.error("http_exception", status_code=exc.status_code, detail=exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error("validation_error", errors=exc.errors())
        return JSONResponse(
            status_code=400,
            content={
                "code": BIZ_INVALID_PARAMS,
                "message": "Invalid request parameters",
                "details": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.exception("unhandled_exception", error=str(exc))
        return JSONResponse(
            status_code=500,
            content={
                "code": 9001,
                "message": "Internal server error",
            },
        )