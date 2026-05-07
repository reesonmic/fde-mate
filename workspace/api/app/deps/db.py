"""
Database Dependencies - async SQLAlchemy support.
"""
from collections.abc import AsyncGenerator
from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config.settings import settings


@lru_cache
def get_async_engine():
    """Get cached async SQLAlchemy engine."""
    url = settings.database_url
    # Ensure async-compatible URL
    if url.startswith("mysql://"):
        url = url.replace("mysql://", "mysql+aiomysql://")
    elif url.startswith("mysql+pymysql://"):
        url = url.replace("mysql+pymysql://", "mysql+aiomysql://")
    elif url.startswith("sqlite://"):
        # SQLite uses aiosqlite for async support
        if not url.startswith("sqlite+aiosqlite://"):
            url = url.replace("sqlite://", "sqlite+aiosqlite://")

    return create_async_engine(
        url,
        pool_pre_ping=True,
        pool_size=10 if "sqlite" not in url else 1,  # SQLite uses single connection
        max_overflow=0 if "sqlite" not in url else 0,
    )


@lru_cache
def get_async_session_factory():
    """Get cached async session factory."""
    return async_sessionmaker(
        bind=get_async_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session dependency."""
    async with get_async_session_factory()() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Alias for get_async_session."""
    async with get_async_session_factory()() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
