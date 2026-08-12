from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services import ChatToUserService
from .database import get_session


def get_chat_to_user_service(
    session: AsyncSession = Depends(get_session),
) -> ChatToUserService:
    return ChatToUserService(session)
