from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services import (
    AuthService,
    ChatManager,
    ChatParticipantService,
    MessageService,
    PrivateChatService,
    PublicChatProfileService,
)
from .auth import get_auth_service
from .database import _get_session
from .messages import get_message_service


def get_public_chat_profile_service(
    session: AsyncSession = Depends(_get_session),
) -> PublicChatProfileService:
    return PublicChatProfileService(session)


def get_private_chat_service(
    session: AsyncSession = Depends(_get_session),
) -> PrivateChatService:
    return PrivateChatService(session)


def get_chat_participant_service(
    session: AsyncSession = Depends(_get_session),
) -> ChatParticipantService:
    return ChatParticipantService(session)


def get_chat_manager(
    session: AsyncSession = Depends(_get_session),
    private_chat_service: PrivateChatService = Depends(get_private_chat_service),
    public_chat_profile_service: PublicChatProfileService = Depends(
        get_public_chat_profile_service
    ),
    message_service: MessageService = Depends(get_message_service),
    auth_service: AuthService = Depends(get_auth_service),
    chat_participant_service: ChatParticipantService = Depends(
        get_chat_participant_service
    ),
) -> ChatManager:
    return ChatManager(
        session=session,
        private_chat_service=private_chat_service,
        public_chat_profile_service=public_chat_profile_service,
        message_service=message_service,
        auth_service=auth_service,
        chat_participant_service=chat_participant_service,
    )
