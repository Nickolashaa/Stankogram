from fastapi import Depends, HTTPException

from ..dependencies import get_chat_manager, get_current_user
from ..schemas.users import UserResponse
from ..services import ChatManager


async def can_read_from_chat(
    chat_id: int,
    user: UserResponse = Depends(get_current_user),
    manager: ChatManager = Depends(get_chat_manager),
) -> None:
    if (
        await manager.can_message_to_chat(
            user_id=user.id,
            chat_id=chat_id,
        )
        is False
    ):
        raise HTTPException(status_code=403, detail="Access denied")


# Реализовать чекбоксы muted и отталкиваться от них, пока что не использовать
async def can_write_to_chat(
    chat_id: int,
    user: UserResponse = Depends(get_current_user),
    manager: ChatManager = Depends(get_chat_manager),
) -> None:
    if (
        await manager.can_message_to_chat(
            user_id=user.id,
            chat_id=chat_id,
        )
        is False
    ):
        raise HTTPException(status_code=403, detail="Access denied")
