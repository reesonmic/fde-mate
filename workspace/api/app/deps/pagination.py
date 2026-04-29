"""
Pagination dependency.
"""
from fastapi import Query


def pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=200, description="Page size"),
) -> dict:
    """Extract pagination parameters."""
    return {"page": page, "size": size}
