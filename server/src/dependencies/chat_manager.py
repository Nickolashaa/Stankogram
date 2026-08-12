from fastapi import Depends

from ..services.chats import ChatManager, ChatService, ChatToUserService
from .chats import get_chat_service
from .chats_to_users import get_chat_to_user_service


def get_chat_manager(
    chat_service: ChatService = Depends(get_chat_service),
    chat_to_user_service: ChatToUserService = Depends(get_chat_to_user_service),
) -> ChatManager:
    return ChatManager(
        chat_service=chat_service,
        chat_to_user_service=chat_to_user_service,
    )
