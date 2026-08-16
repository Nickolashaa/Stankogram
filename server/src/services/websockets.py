from fastapi import WebSocket

from ..schemas.messages import MessageCreate
from ..schemas.users import UserResponse
from ..schemas.websockets import WebSocketSchema
from ..services import ChatService, MessageService


class WebSocketConnectionManager:
    def __init__(
        self, message_service: MessageService, chat_service: ChatService
    ) -> None:
        self._active_connections: dict[int, WebSocket] = {}
        self._message_service = message_service
        self._chat_service = chat_service

    async def connect(self, websocket: WebSocket, user_id: int) -> None:
        await websocket.accept()
        self._active_connections[user_id] = websocket

    async def disconnect(self, user_id: int) -> None:
        self._active_connections.pop(user_id)

    async def send_message(self, websocket: WebSocket, data: WebSocketSchema) -> None:
        await websocket.send_json(data.model_dump_json())

    async def process_event(
        self,
        data: WebSocketSchema,
        user: UserResponse,
    ) -> None:
        if isinstance(data, MessageCreate):
            await self._message_service.create(
                user_id=user.id,
                **data.model_dump(),
            )

            recipient_ids = await self._chat_service.get_recipient_ids(
                chat_id=data.chat_id
            )

            for recipient_id in recipient_ids:
                websocket = self._active_connections.get(recipient_id)
                if websocket is None:
                    ...
                    return
                await self.send_message(
                    websocket=websocket,
                    data=data,
                )
