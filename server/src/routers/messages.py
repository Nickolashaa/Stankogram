from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query

from ..dependencies import get_current_user, get_message_service
from ..schemas.messages import (
    MessageCreate,
    MessageFilters,
    MessageListQuery,
    MessageResponse,
)
from ..schemas.users import UserResponse
from ..services import MessageService
from ..services.exceptions import Forbidden, ObjectNotFound

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/create", response_model=MessageResponse)
async def create(
    data: Annotated[MessageCreate, Body()],
    user: UserResponse = Depends(get_current_user),
    service: MessageService = Depends(get_message_service),
) -> MessageResponse:
    try:
        return await service.create(user_id=user.id, **data.model_dump())
    except (ObjectNotFound, Forbidden) as e:
        raise e.to_http_exception()


@router.get("", response_model=list[MessageResponse])
async def get_list(
    query: Annotated[MessageListQuery, Query()],
    service: MessageService = Depends(get_message_service),
) -> list[MessageResponse]:
    return await service.get_list(
        limit=query.limit,
        offset=query.offset,
        filters=MessageFilters(
            user_id=query.user_id,
            chat_id=query.chat_id,
        ).model_dump(exclude_unset=True),
    )
