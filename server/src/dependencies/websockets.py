from functools import lru_cache

from fastapi import Depends

from ..services import (
    ChatManager,
    ConnectionRegistry,
    WebSocketConnectionManager,
)
from .chats import get_chat_manager


@lru_cache
def get_connection_registry() -> ConnectionRegistry:
    return ConnectionRegistry()


def get_websocket_connection_manager(
    connection_registry: ConnectionRegistry = Depends(get_connection_registry),
    chat_manager: ChatManager = Depends(get_chat_manager),
) -> WebSocketConnectionManager:
    return WebSocketConnectionManager(
        connection_registry=connection_registry,
        chat_manager=chat_manager,
    )
