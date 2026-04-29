"""
Redis Dependencies
"""
from functools import lru_cache

import redis
from redis import Redis

from app.config.settings import settings


@lru_cache
def get_redis_client() -> Redis:
    """Get cached Redis client."""
    return redis.from_url(settings.redis_url, decode_responses=True)


def get_redis() -> Redis:
    """Get Redis client dependency."""
    return get_redis_client()