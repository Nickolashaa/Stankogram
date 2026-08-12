from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services import ChatService
from .database import get_session


def get_chat_service(
    session: AsyncSession = Depends(get_session),
) -> ChatService:
    return ChatService(session)
