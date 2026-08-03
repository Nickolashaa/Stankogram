from fastapi import APIRouter, Depends, Response

from ..config import JWT_REFRESH_EXP_DAYS
from ..dependencies import get_current_user, get_user_service
from ..schemas.jwt import JWTTokens
from ..schemas.users import UserCreate, UserCredentials, UserResponse
from ..services import UserService
from ..services.exceptions import ObjectAlreadyExists, ObjectNotFound

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(
    user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    return user


@router.get("/{id}", response_model=UserResponse)
async def get_user(
    id: int, service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        return await service.get(id)
    except ObjectNotFound as e:
        raise e.to_http_exception()


@router.post("/register", response_model=UserCredentials)
async def register_user(
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
