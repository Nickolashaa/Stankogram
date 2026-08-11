from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services import ChatsService
from .database import get_session


def get_chats_service(
    session: AsyncSession = Depends(get_session),
) -> ChatsService:
    return ChatsService(session)
