from time import time
from typing import NamedTuple
from uuid import uuid4

from redis.asyncio import Redis

from ...config import settings
from ...enums.rate_limit import RateLimitScope


class _Limit(NamedTuple):
    max_hits: int
    window_seconds: int


_LIMITS: dict[RateLimitScope, _Limit] = {
    RateLimitScope.LOGIN_IP: _Limit(
        max_hits=settings.LOGIN_MAX_ATTEMPTS_PER_IP,
        window_seconds=settings.LOGIN_ATTEMPTS_WINDOW_MINUTES * 60,
    ),
    RateLimitScope.LOGIN_EMAIL: _Limit(
        max_hits=settings.LOGIN_MAX_ATTEMPTS_PER_EMAIL,
        window_seconds=settings.LOGIN_ATTEMPTS_WINDOW_MINUTES * 60,
    ),
    RateLimitScope.PASSWORD_RESET_REQUEST: _Limit(
        max_hits=settings.PASSWORD_RESET_REQUEST_MAX_PER_IP,
        window_seconds=settings.PASSWORD_RESET_REQUEST_WINDOW_MINUTES * 60,
    ),
    RateLimitScope.PASSWORD_RESET_CONFIRM: _Limit(
        max_hits=settings.PASSWORD_RESET_CONFIRM_MAX_PER_IP,
        window_seconds=settings.PASSWORD_RESET_CONFIRM_WINDOW_MINUTES * 60,
    ),
}


class RateLimitService:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    @staticmethod
    def _key(scope: RateLimitScope, key: str) -> str:
        return f"rate:{scope}:{key}"

    async def is_blocked(self, scope: RateLimitScope, key: str) -> bool:
        limit = _LIMITS[scope]
        hits = await self._redis.zcount(
            self._key(scope, key),
            time() - limit.window_seconds,
            "+inf",
        )

        return hits >= limit.max_hits

    async def retry_after_seconds(self, scope: RateLimitScope, key: str) -> int:
        limit = _LIMITS[scope]
        oldest = await self._redis.zrangebyscore(
            self._key(scope, key),
            min=time() - limit.window_seconds,
            max="+inf",
            start=0,
            num=1,
            withscores=True,
        )
        if not oldest:
            return 0

        hit_at = float(oldest[0][1])

        return max(1, int(hit_at + limit.window_seconds - time()))

    async def hit(self, scope: RateLimitScope, key: str) -> None:
        limit = _LIMITS[scope]
        redis_key = self._key(scope, key)
        now = time()

        async with self._redis.pipeline() as pipe:
            pipe.zadd(redis_key, {uuid4().hex: now})
            pipe.zremrangebyscore(redis_key, "-inf", now - limit.window_seconds)
            pipe.expire(redis_key, limit.window_seconds)
            await pipe.execute()

    async def reset(self, scope: RateLimitScope, key: str) -> None:
        await self._redis.delete(self._key(scope, key))
