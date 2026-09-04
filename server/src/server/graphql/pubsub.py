from asyncio.queues import Queue

from .types.messages import Message

Event = Message


class PubSub:
    def __init__(self) -> None:
        self._connections: dict[int, Queue[Event | None]] = {}

    def connect(self, user_id: int) -> Queue[Event | None]:
        if (existing := self._connections.get(user_id)) is not None:
            existing.put_nowait(None)
        queue: Queue[Event | None] = Queue()
        self._connections[user_id] = queue
        return queue

    def disconnect(self, user_id: int, queue: Queue[Event | None]) -> None:
        if self._connections.get(user_id) is queue:
            del self._connections[user_id]

    def publish(self, user_id: int, event: Event) -> None:
        if (queue := self._connections.get(user_id)) is not None:
            queue.put_nowait(event)


pub_sub = PubSub()
