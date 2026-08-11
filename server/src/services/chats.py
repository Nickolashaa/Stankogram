from sqlalchemy import delete, insert

from ..database.models.chats import Chat
from ..schemas.chats import ChatInput, ChatResponse
from .base import BaseService


class ChatsService(BaseService):
    async def create(
        self,
        data: ChatInput,
    ) -> ChatResponse:
        stmt = insert(Chat).values(**data.model_dump()).returning(Chat)

        res = await self._session.execute(stmt)

        return ChatResponse.model_validate(res.scalar_one())

    async def delete(
        self,
        id: int,
    ) -> None:
        stmt = delete(Chat).where(Chat.id == id)
        await self._session.execute(stmt)
