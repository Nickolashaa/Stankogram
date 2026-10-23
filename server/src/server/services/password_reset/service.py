from secrets import compare_digest

from redis.asyncio import Redis

from ...config import settings


class PasswordResetService:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    @staticmethod
    def _key(user_id: int) -> str:
        return f"password_reset:{user_id}"

    @staticmethod
    def _cooldown_key(user_id: int) -> str:
        return f"password_reset_cooldown:{user_id}"

    async def in_cooldown(self, user_id: int) -> bool:
        return await self._redis.exists(self._cooldown_key(user_id)) == 1

    async def store(self, user_id: int, code: str) -> None:
        key = self._key(user_id)

        async with self._redis.pipeline() as pipe:
            pipe.delete(key)
            pipe.hset(key, mapping={"code": code, "attempts": 0})
            pipe.expire(key, settings.PASSWORD_RESET_CODE_EXP_MINUTES * 60)
            pipe.set(
                self._cooldown_key(user_id),
                "1",
                ex=settings.PASSWORD_RESET_REQUEST_COOLDOWN_SECONDS,
            )
            await pipe.execute()

    async def verify(self, user_id: int, code: str) -> bool:
        key = self._key(user_id)
        stored = await self._redis.hget(key, "code")
        if stored is None:
            return False

        stored_code = stored if isinstance(stored, bytes) else stored.encode()

        if compare_digest(stored_code, code.encode()):
            await self._redis.delete(key)
            return True

        attempts = await self._redis.hincrby(key, "attempts", 1)
        if attempts >= settings.PASSWORD_RESET_CODE_MAX_ATTEMPTS:
            await self._redis.delete(key)

        return False
