from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services import ChatService
from ..services.users import UserService
from .database import get_session
from .users import get_user_service


def get_chat_service(
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
) -> ChatService:
    return ChatService(
        session=session,
        user_service=user_service,
    )
