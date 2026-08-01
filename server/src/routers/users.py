from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_user_service
from ..schemas.users import UserCreate, UserCredentials, UserResponse
from ..services import UserService
from ..services.exceptions import ObjectAlreadyExists, ObjectNotFound

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{id}", response_model=UserResponse)
async def get_user(
    id: int, service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        return await service.get(id)
    except ObjectNotFound as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post("/register", response_model=UserCredentials)
async def register_user(
    body: UserCreate, service: UserService = Depends(get_user_service)
) -> UserCredentials:
    try:
        return await service.register(body)
    except ObjectAlreadyExists as e:
        raise HTTPException(
            status_code=422,
            detail=str(e),
        )
