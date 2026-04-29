"""
Base ORM models and common mixins.
"""
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, SmallInteger
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class TimestampMixin:
    """Mixin for gmt_create / gmt_modified timestamps."""
    gmt_create = Column(DateTime, nullable=False, default=datetime.utcnow)
    gmt_modified = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class SoftDeleteMixin:
    """Mixin for soft delete."""
    is_deleted = Column(SmallInteger, nullable=False, default=0)
