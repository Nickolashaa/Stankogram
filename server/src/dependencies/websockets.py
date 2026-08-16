from fastapi import Depends

from ..services import ChatService, MessageService
from ..services.websockets import WebSocketConnectionManager
from .chats import get_chat_service
from .messages import get_message_service


def get_websocket_connection_manager(
    message_service: MessageService = Depends(get_message_service),
    chat_service: ChatService = Depends(get_chat_service),
) -> WebSocketConnectionManager:
    return WebSocketConnectionManager(
        message_service=message_service,
        chat_service=chat_service,
    )
