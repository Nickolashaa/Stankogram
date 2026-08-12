from typing import Annotated

from fastapi import APIRouter, Body, Depends

from ..dependencies import get_chat_manager
from ..schemas.chats import ChatResponse, PrivateChatParticipants
from ..services.chats import ChatManager

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/get_private_or_create", response_model=ChatResponse)
async def get_private_or_create(
    data: Annotated[PrivateChatParticipants, Body()],
    manager: ChatManager = Depends(get_chat_manager),
) -> ChatResponse:
    return await manager.get_or_create(
        first_user_id=data.first_user_id,
        second_user_id=data.second_user_id,
    )
