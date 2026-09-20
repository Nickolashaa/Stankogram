from asyncio.queues import Queue
from typing import Any


class PubSub:
    def __init__(self) -> None:
        self._connections: dict[int, Queue[Any]] = {}

    def is_connected(self, user_id: int) -> bool:
        return self._connections.get(user_id) is not None

    def connect(self, user_id: int) -> Queue[Any]:
        if (existing := self._connections.get(user_id)) is not None:
            existing.put_nowait(None)
        queue: Queue[Any] = Queue()
        self._connections[user_id] = queue
        return queue

    def disconnect(self, user_id: int, queue: Queue[Any]) -> bool:
        if self._connections.get(user_id) is not queue:
            return False
        del self._connections[user_id]
        return True

    def publish(self, user_id: int, event: Any) -> None:
        if (queue := self._connections.get(user_id)) is not None:
            queue.put_nowait(event)


pub_sub = PubSub()
