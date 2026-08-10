from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query

from ..dependencies import get_user_service
from ..permissions import is_admin
from ..schemas.base import PaginationSchema
from ..schemas.users import (
    PasswordResetRequest,
    UserFilters,
    UserInput,
    UserListQuery,
    UserResponse,
)
from ..services import UserService
from ..services.exceptions import ObjectAlreadyExists, ObjectNotFound

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse], dependencies=[Depends(is_admin)])
async def get_users(
    query: Annotated[UserListQuery, Query()],
    service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    return await service.get_list(
        filters=query,
        pagination=PaginationSchema(limit=query.limit, offset=query.offset),
    )


@router.get("/count", response_model=int, dependencies=[Depends(is_admin)])
async def get_users_count(
    filters: Annotated[UserFilters, Query()],
    service: UserService = Depends(get_user_service),
) -> int:
    return await service.count(filters)


@router.get("/{id}", response_model=UserResponse, dependencies=[Depends(is_admin)])
async def get_user(
    id: Annotated[int, Path()], service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        return await service.get(id)
    except ObjectNotFound as e:
        raise e.to_http_exception()


@router.post("/create", response_model=UserResponse, dependencies=[Depends(is_admin)])
async def register(
    data: Annotated[UserInput, Body()],
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        return await service.create(data)
    except ObjectAlreadyExists as e:
        raise e.to_http_exception()


@router.delete("/delete", response_model=None, dependencies=[Depends(is_admin)])
async def delete(
    id: Annotated[int, Query()], service: UserService = Depends(get_user_service)
) -> None:
    await service.delete(id)


@router.put(
    "/{id}/update", response_model=UserResponse, dependencies=[Depends(is_admin)]
)
async def update(
    id: Annotated[int, Path()],
    data: Annotated[UserInput, Body()],
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        return await service.update(id=id, data=data)
    except (ObjectNotFound, ObjectAlreadyExists) as e:
        raise e.to_http_exception()


@router.post("/reset_password_request", response_model=None)
async def reset_password_request(
    data: Annotated[PasswordResetRequest, Body()],
    service: UserService = Depends(get_user_service),
) -> None:
    try:
        await service.reset_password_request(data.email)
    except ObjectNotFound as e:
        raise e.to_http_exception()


@router.get("/{id}/reset_password_confirm/{code}", response_model=None)
async def reset_password_confirm(
    id: Annotated[int, Path()],
    code: Annotated[str, Path()],
    service: UserService = Depends(get_user_service),
) -> None:
    try:
        await service.reset_password_confirm(id=id, code=code)
    except ObjectNotFound as e:
        raise e.to_http_exception()
