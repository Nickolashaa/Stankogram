from cryptography.fernet import Fernet
from fastapi import Depends
from redis.asyncio import Redis

from ..services.events import EventService
from .encryption import get_fernet
from .redis import get_redis


def get_event_service(
    redis: Redis = Depends(get_redis),
    fernet: Fernet = Depends(get_fernet),
) -> EventService:
    return EventService(redis=redis, fernet=fernet)
