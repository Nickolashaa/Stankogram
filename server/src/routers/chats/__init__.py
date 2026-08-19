from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from ...dependencies import get_chat_manager
from ...permissions import can_read_from_chat
from ...schemas.base import PaginationSchema
from ...schemas.messages import MessageProfile
from ...services import ChatManager
from .private import router as private_chats_router

router = APIRouter(prefix="/chats", tags=["chats"])
router.include_router(private_chats_router)


@router.get(
    "/{id}/messages",
    response_model=list[MessageProfile],
    dependencies=[Depends(can_read_from_chat)],
)
async def get_messages(
    chat_id: Annotated[int, Path()],
    query: Annotated[PaginationSchema, Query()],
    manager: ChatManager = Depends(get_chat_manager),
) -> list[MessageProfile]:
    return await manager.get_messages(
        limit=query.limit,
        offset=query.offset,
        chat_id=chat_id,
    )
