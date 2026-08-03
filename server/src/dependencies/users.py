import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.users import UserJWTPayload, UserResponse
from ..services import UserService
from ..services.exceptions import ObjectNotFound
from .database import get_session


def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    return UserService(session)


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

    try:
        return await service.get(payload.id)
    except ObjectNotFound as e:
        raise e.to_http_exception()
