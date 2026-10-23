from fastapi import Depends
from redis.asyncio import Redis

from ..services.presence import PresenceService
from .redis import get_redis


def get_presence_service(
    redis: Redis = Depends(get_redis),
) -> PresenceService:
    return PresenceService(redis)
