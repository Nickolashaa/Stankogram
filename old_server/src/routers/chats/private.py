from typing import Annotated

from fastapi import APIRouter, Body, Depends

from ...dependencies import get_chat_manager, get_current_user
from ...exceptions import InvalidInput, ObjectNotFound
from ...schemas.chats import ChatProfile
from ...schemas.users import UserResponse
from ...services.chats import ChatManager

router = APIRouter(prefix="/private")


@router.post("/get_or_create", response_model=ChatProfile)
async def get_private_or_create(
    participant_id: Annotated[int, Body()],
    user: UserResponse = Depends(get_current_user),
    manager: ChatManager = Depends(get_chat_manager),
) -> ChatProfile:
    try:
        return await manager.get_or_create_private_chat(
            user_id=user.id,
            participant_id=participant_id,
        )
    except (ObjectNotFound, InvalidInput) as e:
        raise e.to_http_exception()
