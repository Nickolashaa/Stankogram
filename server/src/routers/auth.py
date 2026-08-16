from typing import Annotated
from uuid import UUID

import jwt
from fastapi import (
    APIRouter,
    Body,
    Cookie,
    Depends,
    HTTPException,
    Path,
    Query,
    Response,
)

from ..config import JWT_REFRESH_EXP_DAYS
from ..dependencies import (
    get_auth_service,
    get_current_user,
)
from ..exceptions import ObjectAlreadyExists, ObjectNotFound
from ..permissions import is_admin
from ..schemas.jwt import JWTTokens, UserJWTPayload
from ..schemas.users import (
    PasswordResetConfirm,
    PasswordResetRequest,
    UserCredentials,
    UserFilters,
    UserInput,
    UserListQuery,
    UserResponse,
)
from ..services import AuthService

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
) -> JWTTokens:
    try:
        user = await service.login(**credentials.model_dump())
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
        user = await service.get(payload.id)
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


@router.get("", response_model=list[UserResponse])
async def get_users(
    query: Annotated[UserListQuery, Query()],
    service: AuthService = Depends(get_auth_service),
) -> list[UserResponse]:
    return await service.get_list(
        limit=query.limit,
        offset=query.offset,
        filters=UserFilters(
            search_query=query.search_query, role=query.role, is_admin=query.is_admin
        ).model_dump(exclude_unset=True),
    )


@router.get("/count", response_model=int)
async def get_users_count(
    filters: Annotated[UserFilters, Query()],
    service: AuthService = Depends(get_auth_service),
) -> int:
    return await service.count(**filters.model_dump(exclude_unset=True))


@router.get("/{id}", response_model=UserResponse, dependencies=[Depends(is_admin)])
async def get_user(
    id: Annotated[int, Path()], service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    try:
        return await service.get(id)
    except ObjectNotFound as e:
        raise e.to_http_exception()


@router.post("/create", response_model=UserResponse, dependencies=[Depends(is_admin)])
async def register(
    data: Annotated[UserInput, Body()],
    service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    try:
        return await service.create(**data.model_dump())
    except ObjectAlreadyExists as e:
        raise e.to_http_exception()


@router.delete("/delete", response_model=None, dependencies=[Depends(is_admin)])
async def delete(
    id: Annotated[int, Query()], service: AuthService = Depends(get_auth_service)
) -> None:
    await service.delete(id)


@router.put(
    "/{id}/update", response_model=UserResponse, dependencies=[Depends(is_admin)]
)
async def update(
    id: Annotated[int, Path()],
    data: Annotated[UserInput, Body()],
    service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    try:
        return await service.update(id=id, **data.model_dump())
    except (ObjectNotFound, ObjectAlreadyExists) as e:
        raise e.to_http_exception()


@router.post("/reset_password_request", response_model=None)
async def reset_password_request(
    data: Annotated[PasswordResetRequest, Body()],
    service: AuthService = Depends(get_auth_service),
) -> None:
    try:
        await service.reset_password_request(data.email)
    except ObjectNotFound as e:
        raise e.to_http_exception()


@router.post("/reset_password_confirm", response_model=None)
async def reset_password_confirm(
    data: Annotated[PasswordResetConfirm, Body()],
    service: AuthService = Depends(get_auth_service),
) -> None:
    try:
        await service.reset_password_confirm(id=data.id, code=data.code)
    except ObjectNotFound as e:
        raise e.to_http_exception()
