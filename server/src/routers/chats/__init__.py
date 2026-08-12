from fastapi import APIRouter, Depends

from ...dependencies import get_chat_service, get_current_user
from ...schemas.chats import ChatProfileResponse
from ...schemas.users import UserResponse
from ...services.chats import ChatService
from .private import router as private_chats_router

router = APIRouter(prefix="/chats", tags=["chats"])
router.include_router(private_chats_router)


@router.get("", response_model=list[ChatProfileResponse])
async def get_list(
    user: UserResponse = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
) -> list[ChatProfileResponse]:
    return await service.get_list(user_id=user.id)
