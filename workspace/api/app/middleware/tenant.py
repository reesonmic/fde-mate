"""
Tenant Middleware for Multi-tenancy
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from structlog.contextvars import bind_contextvars


class TenantMiddleware(BaseHTTPMiddleware):
    """Handle multi-tenant context from request headers."""

    async def dispatch(self, request: Request, call_next):
        # Extract tenant ID from headers (if applicable)
        tenant_id = request.headers.get("X-Tenant-ID", "default")

        # Bind to structlog context
        bind_contextvars(tenant_id=tenant_id)

        response: Response = await call_next(request)

        return response