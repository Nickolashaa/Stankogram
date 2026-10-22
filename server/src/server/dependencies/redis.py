from redis.asyncio import Redis

from ..redis.connection import redis_client


def get_redis() -> Redis:
    return redis_client
