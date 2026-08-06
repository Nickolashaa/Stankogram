import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.jwt import UserJWTPayload
from ..schemas.users import UserResponse
from ..services import AuthService, UserService
from ..services.exceptions import ObjectNotFound
from .database import get_session
from .users import get_user_service


def get_auth_service(
    session: AsyncSession = Depends(get_session),
) -> AuthService:
    return AuthService(session)


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        payload = UserJWTPayload.from_token(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.type == "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    try:
        return await service.get(payload.id)
    except ObjectNotFound as e:
        raise e.to_http_exception()


async def is_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> None:
    try:
        payload = UserJWTPayload.from_token(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.type == "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    if payload.is_admin is False:
        raise HTTPException(status_code=403, detail="Access denied")
