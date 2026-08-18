from fastapi import WebSocket

from ..exceptions import AppException
from ..schemas.messages import MessageCreate
from ..schemas.users import UserResponse
from ..schemas.websockets import WebSocketSchema
from .chats import ChatManager


class ConnectionRegistry:
    def __init__(self) -> None:
        self._active_connections: dict[int, WebSocket] = {}

    def add(self, user_id: int, websocket: WebSocket) -> None:
        self._active_connections[user_id] = websocket

    def remove(self, user_id: int) -> None:
        self._active_connections.pop(user_id, None)

    def get(self, user_id: int) -> WebSocket | None:
        return self._active_connections.get(user_id)


class WebSocketConnectionManager:
    def __init__(
        self,
        connection_registry: ConnectionRegistry,
        chat_manager: ChatManager,
    ) -> None:
        self._connections = connection_registry
        self._chat_manager = chat_manager

    async def connect(self, websocket: WebSocket, user_id: int) -> None:
        await websocket.accept()
        self._connections.add(user_id, websocket)

    def disconnect(self, user_id: int) -> None:
        self._connections.remove(user_id)

    async def process_event(
        self,
        data: WebSocketSchema,
        user: UserResponse,
    ) -> None:
        if isinstance(data, MessageCreate):
            try:
                message = await self._chat_manager.send_message(
                    user_id=user.id,
                    **data.model_dump(),
                )
            except AppException:
                raise

            recipient_ids = await self._chat_manager.get_recipient_ids(
                chat_id=data.chat_id
            )

            for recipient_id in recipient_ids:
                websocket = self._connections.get(recipient_id)
                if websocket is None:
                    continue
                await websocket.send_json(message.model_dump(mode="json"))
