from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.auth import AuthService
from ..services.auth.schemas import UserResponse
from ..services.exceptions import ObjectNotFound, Unauthorized
from .session import get_session


def get_auth_service(
    session: AsyncSession = Depends(get_session),
) -> AuthService:
    return AuthService(session)


async def get_user_from_authorization(
    authorization: str | None,
    service: AuthService,
) -> UserResponse | None:
    if authorization is None:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    try:
        return await service.get_from_token(token)
    except Unauthorized, ObjectNotFound:
        return None


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    service: AuthService = Depends(get_auth_service),
) -> UserResponse | None:
    return await get_user_from_authorization(authorization, service)
