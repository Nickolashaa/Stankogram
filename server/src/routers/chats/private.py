from typing import Annotated

from fastapi import APIRouter, Body, Depends

from ...dependencies import get_chat_service, get_current_user
from ...exceptions import InvalidInput, ObjectNotFound
from ...schemas.chats import ChatResponse
from ...schemas.users import UserResponse
from ...services.chats import ChatService

router = APIRouter(prefix="/private")


@router.post("/get_or_create", response_model=ChatResponse)
async def get_private_or_create(
    participant_id: Annotated[int, Body()],
    user: UserResponse = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    try:
        return await service.get_private_chat_or_create(
            my_id=user.id,
            participant_id=participant_id,
        )
    except (ObjectNotFound, InvalidInput) as e:
        raise e.to_http_exception()
