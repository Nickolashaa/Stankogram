from typing import Unpack

from sqlalchemy import delete, insert, select

from ...database.models.chats import Chat
from ...schemas.chats import ChatResponse
from ..base import BaseService
from ..exceptions import ObjectNotFound
from .types import ChatCreateParams


class ChatService(BaseService):
    async def create(
        self,
        **values: Unpack[ChatCreateParams],
    ) -> ChatResponse:
        stmt = insert(Chat).values(**values).returning(Chat)

        res = await self._session.execute(stmt)

        return ChatResponse.model_validate(res.scalar_one())

    async def get(
        self,
        id: int,
    ) -> ChatResponse:
        stmt = select(Chat).where(Chat.id == id)
        res = await self._session.execute(stmt)
        entity = res.scalar_one_or_none()
        if entity is None:
            raise ObjectNotFound(f"Chat with id {id} not found")
        return ChatResponse.model_validate(entity)

    async def delete(
        self,
        id: int,
    ) -> None:
        stmt = delete(Chat).where(Chat.id == id)
        await self._session.execute(stmt)
