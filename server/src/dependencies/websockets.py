from functools import lru_cache

from fastapi import Depends

from ..services import (
    ChatService,
    ConnectionRegistry,
    MessageService,
    WebSocketConnectionManager,
)
from .chats import get_chat_service
from .messages import get_message_service


@lru_cache
def get_connection_registry() -> ConnectionRegistry:
    return ConnectionRegistry()


def get_websocket_connection_manager(
    message_service: MessageService = Depends(get_message_service),
    chat_service: ChatService = Depends(get_chat_service),
    connection_registry: ConnectionRegistry = Depends(get_connection_registry),
) -> WebSocketConnectionManager:
    return WebSocketConnectionManager(
        message_service=message_service,
        chat_service=chat_service,
        connection_registry=connection_registry,
    )
