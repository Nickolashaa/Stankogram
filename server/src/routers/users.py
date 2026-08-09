from fastapi import APIRouter, Depends

from ..config import LIMIT, OFFSET
from ..dependencies import get_user_service, is_admin
from ..schemas.users import UserCreate, UserCredentials, UserFilters, UserResponse
from ..services import UserService
from ..services.exceptions import ObjectAlreadyExists, ObjectNotFound

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(is_admin)])


@router.get("/{id}", response_model=UserResponse)
async def get_user(
    id: int, service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        return await service.get(id)
    except ObjectNotFound as e:
        raise e.to_http_exception()


@router.get("", response_model=list[UserResponse])
async def get_users(
    filters: UserFilters | None = None,
    limit: int | None = LIMIT,
    offset: int | None = OFFSET,
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    return await service.get_list(
        filters=filters,
        limit=limit,
        offset=offset,
    )


@router.get("/count", response_model=int)
async def get_users_count(
    filters: UserFilters | None = None,
    service: UserService = Depends(get_user_service),
) -> int:
    return await service.count(filters)


@router.post("/create", response_model=UserCredentials)
async def register(
    data: UserCreate, service: UserService = Depends(get_user_service)
) -> UserCredentials:
    try:
        return await service.create(data)
    except ObjectAlreadyExists as e:
        raise e.to_http_exception()
