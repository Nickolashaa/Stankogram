from typing import Annotated
from uuid import UUID

import jwt
from fastapi import APIRouter, Body, Cookie, Depends, HTTPException, Response

from ..config import JWT_REFRESH_EXP_DAYS
from ..dependencies import (
    get_auth_service,
    get_current_user,
    get_user_service,
)
from ..schemas.jwt import JWTTokens, UserJWTPayload
from ..schemas.users import UserCredentials, UserResponse
from ..services import AuthService, UserService
from ..services.exceptions import ObjectAlreadyExists, ObjectNotFound

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=UserResponse)
async def get_me(
    user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    return user


@router.post("/login", response_model=JWTTokens)
async def login(
    response: Response,
    credentials: Annotated[UserCredentials, Body()],
    service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
) -> JWTTokens:
    try:
        user = await user_service.login(**credentials.model_dump())
    except ObjectNotFound as e:
        raise e.to_http_exception()

    tokens = service.generate_jwt_tokens(id=user.id, is_admin=user.is_admin)

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * JWT_REFRESH_EXP_DAYS,
    )

    return tokens


@router.post("/logout", response_model=None)
async def logout(
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    service: AuthService = Depends(get_auth_service),
) -> None:
    if refresh_token is not None:
        response.delete_cookie("refresh_token")

        try:
            payload = UserJWTPayload.from_token(refresh_token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        await service.cancel_token(UUID(payload.jti))


@router.post("/refresh", response_model=JWTTokens)
async def refresh(
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
) -> JWTTokens:
    if refresh_token is None:
        raise HTTPException(status_code=404, detail="Token not found")

    try:
        payload = UserJWTPayload.from_token(refresh_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.type != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    response.delete_cookie("refresh_token")

    try:
        await service.cancel_token(UUID(payload.jti))
    except ObjectAlreadyExists:
        raise HTTPException(status_code=401, detail="Token in blacklist")

    try:
        user = await user_service.get(payload.id)
    except ObjectNotFound as e:
        raise e.to_http_exception()

    tokens = service.generate_jwt_tokens(id=user.id, is_admin=user.is_admin)

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * JWT_REFRESH_EXP_DAYS,
    )

    return tokens
