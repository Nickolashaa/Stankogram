from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import ObjectNotFound, Unauthorized
from ..schemas.users import UserResponse
from ..services import AuthService
from .database import _get_session


def get_auth_service(
    session: AsyncSession = Depends(_get_session),
) -> AuthService:
    return AuthService(session)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    try:
        return await service.get_from_token(credentials.credentials)
    except (Unauthorized, ObjectNotFound) as e:
        raise e.to_http_exception()
