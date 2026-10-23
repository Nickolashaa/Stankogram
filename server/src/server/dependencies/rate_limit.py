from fastapi import Depends
from redis.asyncio import Redis

from ..services.rate_limit import RateLimitService
from .redis import get_redis


def get_rate_limit_service(
    redis: Redis = Depends(get_redis),
) -> RateLimitService:
    return RateLimitService(redis)
