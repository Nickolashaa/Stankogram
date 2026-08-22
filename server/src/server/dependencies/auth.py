from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.auth import AuthService
from ..services.auth.schemas import UserResponse
from ..services.exceptions import ObjectNotFound, Unauthorized
from .session import get_session


def get_auth_service(
    session: AsyncSession = Depends(get_session),
) -> AuthService:
    return AuthService(session)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        HTTPBearer(auto_error=False)
    ),
    service: AuthService = Depends(get_auth_service),
) -> UserResponse | None:
    if credentials is None:
        return None
    try:
        return await service.get_from_token(credentials.credentials)
    except Unauthorized, ObjectNotFound:
        return None
