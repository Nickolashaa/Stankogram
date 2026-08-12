from typing import Unpack

from sqlalchemy import delete, insert

from ...database.models.chats import Chat
from ...schemas.chats import ChatResponse
from ..base import BaseService
from .types import ChatCreateParams


class ChatService(BaseService):
    async def create(
        self,
        **values: Unpack[ChatCreateParams],
    ) -> ChatResponse:
        stmt = insert(Chat).values(**values).returning(Chat)

        res = await self._session.execute(stmt)

        return ChatResponse.model_validate(res.scalar_one())

    async def delete(
        self,
        id: int,
    ) -> None:
        stmt = delete(Chat).where(Chat.id == id)
        await self._session.execute(stmt)
