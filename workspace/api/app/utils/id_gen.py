"""
ID generation utilities.
"""
import uuid
from datetime import datetime


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


def generate_short_id() -> str:
    """Generate a short unique ID."""
    return uuid.uuid4().hex[:12]


def generate_trace_id() -> str:
    """Generate a trace ID."""
    return uuid.uuid4().hex
