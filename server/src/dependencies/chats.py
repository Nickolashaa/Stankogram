from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services import ChatService
from ..services.auth import AuthService
from .auth import get_auth_service
from .database import get_session


def get_chat_service(
    session: AsyncSession = Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service),
) -> ChatService:
    return ChatService(
        session=session,
        auth_service=auth_service,
    )
