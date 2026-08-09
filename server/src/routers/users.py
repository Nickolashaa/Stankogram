from fastapi import APIRouter, Depends

from ..config import LIMIT, OFFSET
from ..dependencies import get_user_service
from ..permissions import is_admin
from ..schemas.users import UserCredentials, UserFilters, UserInput, UserResponse
from ..services import UserService
from ..services.exceptions import ObjectAlreadyExists, ObjectNotFound

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{id}", response_model=UserResponse, dependencies=[Depends(is_admin)])
async def get_user(
    id: int, service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        return await service.get(id)
    except ObjectNotFound as e:
        raise e.to_http_exception()


@router.get("", response_model=list[UserResponse], dependencies=[Depends(is_admin)])
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


@router.get("/count", response_model=int, dependencies=[Depends(is_admin)])
async def get_users_count(
    filters: UserFilters | None = None,
    service: UserService = Depends(get_user_service),
) -> int:
    return await service.count(filters)


@router.post(
    "/create", response_model=UserCredentials, dependencies=[Depends(is_admin)]
)
async def register(
    data: UserInput, service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        return await service.create(data)
    except ObjectAlreadyExists as e:
        raise e.to_http_exception()


@router.delete("/delete", response_model=None, dependencies=[Depends(is_admin)])
async def delete(id: int, service: UserService = Depends(get_user_service)) -> None:
    await service.delete(id)


@router.put(
    "/{id}/update", response_model=UserResponse, dependencies=[Depends(is_admin)]
)
async def update(
    id: int,
    data: UserInput,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        return await service.update(id=id, data=data)
    except (ObjectNotFound, ObjectAlreadyExists) as e:
        raise e.to_http_exception()


@router.post("/{id}/reset_password_request", response_model=None)
async def reset_password_request(
    id: int,
    service: UserService = Depends(get_user_service),
) -> None:
    await service.reset_password_request(id)


@router.get("/{id}/reset_password_confirm/{code}", response_model=None)
async def reset_password_confirm(
    id: int,
    code: str,
    service: UserService = Depends(get_user_service),
) -> None:
    try:
        await service.reset_password_confirm(id=id, code=code)
    except ObjectNotFound as e:
        raise e.to_http_exception()
