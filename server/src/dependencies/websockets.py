from fastapi import Depends

from ..services import (
    ChatService,
    DeferredMessageEventService,
    MessageService,
    WebSocketConnectionManager,
)
from .chats import get_chat_service
from .deferred_message_events import get_deferred_message_event_service
from .messages import get_message_service


def get_websocket_connection_manager(
    message_service: MessageService = Depends(get_message_service),
    chat_service: ChatService = Depends(get_chat_service),
    deferred_message_event_service: DeferredMessageEventService = Depends(
        get_deferred_message_event_service
    ),
) -> WebSocketConnectionManager:
    return WebSocketConnectionManager(
        message_service=message_service,
        chat_service=chat_service,
        deferred_message_event_service=deferred_message_event_service,
    )
