import asyncio
from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager, suppress
from time import time
from uuid import uuid4

from redis.asyncio import Redis

from ...config import settings


class PresenceService:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    @staticmethod
    def _key(user_id: int) -> str:
        return f"presence:{user_id}"

    @asynccontextmanager
    async def track(self, user_id: int) -> AsyncGenerator[None, None]:
        connection_id = uuid4().hex
        await self._touch(user_id, connection_id)
        heartbeat = asyncio.create_task(self._heartbeat(user_id, connection_id))

        try:
            yield
        finally:
            heartbeat.cancel()
            with suppress(asyncio.CancelledError):
                await heartbeat
            await self._release(user_id, connection_id)

    async def are_online(self, user_ids: Sequence[int]) -> list[bool]:
        threshold = time() - settings.PRESENCE_TTL_SECONDS

        async with self._redis.pipeline() as pipe:
            for user_id in user_ids:
                pipe.zcount(self._key(user_id), threshold, "+inf")
            counts = await pipe.execute()

        return [count > 0 for count in counts]

    async def _touch(self, user_id: int, connection_id: str) -> None:
        key = self._key(user_id)
        now = time()

        async with self._redis.pipeline() as pipe:
            pipe.zadd(key, {connection_id: now})
            pipe.zremrangebyscore(key, "-inf", now - settings.PRESENCE_TTL_SECONDS)
            pipe.expire(key, settings.PRESENCE_TTL_SECONDS * 2)
            await pipe.execute()

    async def _heartbeat(self, user_id: int, connection_id: str) -> None:
        while True:
            await asyncio.sleep(settings.PRESENCE_HEARTBEAT_SECONDS)
            await self._touch(user_id, connection_id)

    async def _release(self, user_id: int, connection_id: str) -> None:
        await self._redis.zrem(self._key(user_id), connection_id)
