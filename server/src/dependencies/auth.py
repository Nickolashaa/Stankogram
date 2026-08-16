import jwt
from fastapi import Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.jwt import UserJWTPayload
from ..schemas.users import UserResponse
from ..services import AuthService
from ..services.exceptions import ObjectNotFound
from .database import get_session


def get_auth_service(
    session: AsyncSession = Depends(get_session),
) -> AuthService:
    return AuthService(session)


async def _get_user_from_token(
    token: str,
    service: AuthService,
) -> UserResponse:
    try:
        payload = UserJWTPayload.from_token(token)
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


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    return await _get_user_from_token(
        token=credentials.credentials,
        service=service,
    )


async def get_current_user_ws(
    token: str = Query(),
    service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    return await _get_user_from_token(
        token=token,
        service=service,
    )
