from fastapi import Depends, HTTPException

from ..dependencies import get_chat_service, get_current_user
from ..schemas.users import UserResponse
from ..services import ChatService


async def can_read_from_chat(
    chat_id: int,
    user: UserResponse = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
) -> None:
    if (
        await service.is_exists(
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
    service: ChatService = Depends(get_chat_service),
) -> bool:
    return await service.is_exists(
        user_id=user.id,
        chat_id=chat_id,
    )
