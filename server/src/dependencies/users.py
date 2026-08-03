import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import JWT_ENCRYPTION_ALGORITHM, JWT_SECRET_KEY
from ..schemas.users import UserJWTAccessPayload, UserResponse
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
        payload = UserJWTAccessPayload.model_validate(
            jwt.decode(
                jwt=credentials.credentials,
                key=JWT_SECRET_KEY,
                algorithms=[JWT_ENCRYPTION_ALGORITHM],
            )
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        return await service.get(payload.id)
    except ObjectNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
