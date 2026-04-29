"""
Trace ID Middleware for Request Tracking
"""
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from structlog.contextvars import bind_contextvars, clear_contextvars


class TraceMiddleware(BaseHTTPMiddleware):
    """Add trace ID to each request for distributed tracing."""

    async def dispatch(self, request: Request, call_next):
        # Generate or extract trace ID
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))

        # Bind to structlog context
        bind_contextvars(trace_id=trace_id)

        response: Response = await call_next(request)

        # Add trace ID to response headers
        response.headers["X-Trace-ID"] = trace_id

        # Clear context vars
        clear_contextvars()

        return response