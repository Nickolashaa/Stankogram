from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services import UsersToChatsService
from .database import get_session


def get_users_to_chats_service(
    session: AsyncSession = Depends(get_session),
) -> UsersToChatsService:
    return UsersToChatsService(session)
