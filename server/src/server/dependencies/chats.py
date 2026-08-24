from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.chats import ChatService
from ..services.chats.participants import ChatParticipantService
from .session import get_session


async def get_chat_service(
    session: AsyncSession = Depends(get_session),
) -> ChatService:
    return ChatService(session)


async def get_chat_participant_service(
    session: AsyncSession = Depends(get_session),
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatParticipantService:
    return ChatParticipantService(
        session=session,
        chat_service=chat_service,
    )
