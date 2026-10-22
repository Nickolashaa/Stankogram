from collections.abc import AsyncGenerator, Sequence

from cryptography.fernet import Fernet
from redis.asyncio import Redis

from .schemas import MessageEventSchema


class EventService:
    def __init__(self, redis: Redis, fernet: Fernet) -> None:
        self._redis = redis
        self._fernet = fernet

    @staticmethod
    def _channel(user_id: int) -> str:
        return f"events:{user_id}"

    async def publish(
        self,
        user_ids: Sequence[int],
        event: MessageEventSchema,
    ) -> None:
        payload = self._fernet.encrypt(event.model_dump_json().encode())

        async with self._redis.pipeline() as pipe:
            for user_id in user_ids:
                pipe.publish(self._channel(user_id), payload)
            await pipe.execute()

    async def listen(self, user_id: int) -> AsyncGenerator[MessageEventSchema, None]:
        async with self._redis.pubsub() as subscription:
            await subscription.subscribe(self._channel(user_id))

            while True:
                message = await subscription.get_message(
                    ignore_subscribe_messages=True,
                    timeout=None,
                )
                if message is None:
                    continue

                yield MessageEventSchema.model_validate_json(
                    self._fernet.decrypt(message["data"])
                )
