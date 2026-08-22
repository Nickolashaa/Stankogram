from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.chats import ChatService
from .session import get_session


async def get_chat_service(
    session: AsyncSession = Depends(get_session),
) -> ChatService:
    return ChatService(session)
