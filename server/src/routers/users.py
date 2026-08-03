from fastapi import APIRouter, Depends

from ..dependencies import get_user_service
from ..schemas.users import UserResponse
from ..services import UserService
from ..services.exceptions import ObjectNotFound

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{id}", response_model=UserResponse)
async def get_user(
    id: int, service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        return await service.get(id)
    except ObjectNotFound as e:
        raise e.to_http_exception()
