from fastapi import APIRouter, Depends

from ..dependencies import get_user_service, is_admin
from ..schemas.users import UserCreate, UserCredentials, UserResponse
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


@router.post("/create", response_model=UserCredentials)
async def register(
    data: UserCreate, service: UserService = Depends(get_user_service)
) -> UserCredentials:
    try:
        return await service.create(data)
    except ObjectAlreadyExists as e:
        raise e.to_http_exception()
