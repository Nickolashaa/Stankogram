from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services import UserService
from .database import get_session


def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    return UserService(session)
