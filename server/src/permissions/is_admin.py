import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..schemas.jwt import UserJWTPayload

security = HTTPBearer()


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
