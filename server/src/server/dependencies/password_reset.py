from fastapi import Depends
from redis.asyncio import Redis

from ..services.password_reset import PasswordResetService
from .redis import get_redis


def get_password_reset_service(
    redis: Redis = Depends(get_redis),
) -> PasswordResetService:
    return PasswordResetService(redis)
