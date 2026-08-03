from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Cookie, Depends, Response

from ..config import JWT_REFRESH_EXP_DAYS
from ..dependencies import (
    get_cancelled_refresh_token_service,
    get_current_user,
    get_user_service,
)
from ..schemas.jwt import JWTTokens
from ..schemas.users import UserCreate, UserCredentials, UserJWTPayload, UserResponse
from ..services import UserService
from ..services.cancelled_refresh_tokens import CancelledRefreshTokenService
from ..services.exceptions import ObjectAlreadyExists, ObjectNotFound

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=UserResponse)
async def get_me(
    user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    return user


@router.post("/register", response_model=UserCredentials)
async def register(
    body: UserCreate, service: UserService = Depends(get_user_service)
) -> UserCredentials:
    try:
        return await service.register(body)
    except ObjectAlreadyExists as e:
        raise e.to_http_exception()


@router.post("/login", response_model=JWTTokens)
async def login(
    response: Response,
    credentials: UserCredentials,
    service: UserService = Depends(get_user_service),
) -> JWTTokens:
    try:
        tokens = await service.login(credentials)
    except ObjectNotFound as e:
        raise e.to_http_exception()

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
    service: CancelledRefreshTokenService = Depends(
        get_cancelled_refresh_token_service
    ),
) -> None:
    if refresh_token is not None:
        response.delete_cookie("refresh_token")

        payload = UserJWTPayload.from_token(refresh_token)

        await service.create(UUID(payload.jti))
