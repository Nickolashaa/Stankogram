from typing import Annotated

from fastapi import APIRouter, Body, Depends

from ..dependencies import get_chat_service
from ..schemas.chats import ChatResponse, PrivateChatParticipants
from ..services.chats import ChatService
from ..services.exceptions import InvalidInputData, ObjectNotFound

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/get_private_or_create", response_model=ChatResponse)
async def get_private_or_create(
    data: Annotated[PrivateChatParticipants, Body()],
    service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    try:
        return await service.get_private_chat_or_create(data.participant_ids)
    except (InvalidInputData, ObjectNotFound) as e:
        raise e.to_http_exception()
