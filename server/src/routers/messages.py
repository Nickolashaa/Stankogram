from typing import Annotated

from fastapi import APIRouter, Depends, Query

from ..dependencies import get_message_service
from ..permissions import can_read_from_chat
from ..schemas.messages import MessageFilters, MessageListQuery, MessageResponse
from ..services import MessageService

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get(
    "", response_model=list[MessageResponse], dependencies=[Depends(can_read_from_chat)]
)
async def get_messages(
    query: Annotated[MessageListQuery, Query()],
    service: MessageService = Depends(get_message_service),
) -> list[MessageResponse]:
    return await service.get_list(
        limit=query.limit,
        offset=query.offset,
        **MessageFilters(
            chat_id=query.chat_id,
        ).model_dump(exclude_unset=True),
    )
