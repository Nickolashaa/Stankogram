from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services import (
    AuthService,
    ChatManager,
    MessageService,
    PrivateChatService,
    PublicChatService,
)
from .auth import get_auth_service
from .database import get_session
from .messages import get_message_service


def get_public_chat_service(
    session: AsyncSession = Depends(get_session),
) -> PublicChatService:
    return PublicChatService(session)


def get_private_chat_service(
    session: AsyncSession = Depends(get_session),
) -> PrivateChatService:
    return PrivateChatService(session)


def get_chat_manager(
    session: AsyncSession = Depends(get_session),
    private_chat_service: PrivateChatService = Depends(get_private_chat_service),
    public_chat_service: PublicChatService = Depends(get_public_chat_service),
    message_service: MessageService = Depends(get_message_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> ChatManager:
    return ChatManager(
        session=session,
        private_chat_service=private_chat_service,
        public_chat_service=public_chat_service,
        message_service=message_service,
        auth_service=auth_service,
    )
