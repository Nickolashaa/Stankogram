from typing import Unpack

from sqlalchemy import Select, delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError

from ...database.models.chats import Chat
from ...database.models.messages import Message
from ...enums.chats import ChatType
from ..base import BasePagination, BaseService
from ..exceptions import InvalidInput, ObjectNotFound
from .schemas import ChatResponse
from .types import ChatCreateParams, ChatGetListFilters, ChatUpdateParams


class ChatService(BaseService):
    async def create(self, **data: Unpack[ChatCreateParams]) -> ChatResponse:
        if data.get("type") == ChatType.PRIVATE and data.get("title") is not None:
            raise InvalidInput("Private chat cannot have title")

        if data.get("type") == ChatType.PUBLIC and data.get("title") is None:
            raise InvalidInput("Public chat must have title")

        stmt = insert(Chat).values(**data).returning(Chat)

        res = await self._session.execute(stmt)

        return ChatResponse.model_validate(res.scalar_one())

    async def get(
        self,
        id: int,
    ) -> ChatResponse:
        stmt = select(Chat).where(Chat.id == id)

        try:
            res = await self._session.execute(stmt)
        except IntegrityError:
            raise ObjectNotFound(f"Chat with id {id} not found")

        return ChatResponse.model_validate(res.scalar_one())

    async def update(
        self,
        id: int,
        **data: Unpack[ChatUpdateParams],
    ) -> ChatResponse:
        chat = await self.get(id)
        if chat.type == ChatType.PRIVATE:
            raise InvalidInput("Private chat cannot have title")

        stmt = update(Chat).where(Chat.id == id).values(**data).returning(Chat)

        res = await self._session.execute(stmt)

        return ChatResponse.model_validate(res.scalar_one())

    async def delete(
        self,
        id: int,
    ) -> None:
        stmt = delete(Chat).where(Chat.id == id)

        await self._session.execute(stmt)

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[Chat]],
        **filters: Unpack[ChatGetListFilters],
    ) -> Select[tuple[Chat]]:
        if (type := filters.get("type")) is not None:
            stmt = stmt.where(Chat.type == type)

        if (ids := filters.get("ids")) is not None:
            stmt = stmt.where(Chat.id.in_(ids))

        return stmt

    async def get_list(
        self,
        pagination: BasePagination | None = None,
        **filters: Unpack[ChatGetListFilters],
    ) -> list[ChatResponse]:
        last_message_at = (
            select(
                Message.chat_id,
                func.max(Message.created_at).label("last_message_at"),
            )
            .group_by(Message.chat_id)
            .subquery()
        )

        stmt = select(Chat).outerjoin(
            last_message_at, last_message_at.c.chat_id == Chat.id
        )

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = stmt.order_by(
            func.coalesce(last_message_at.c.last_message_at, Chat.created_at).desc()
        )

        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        res = await self._session.execute(stmt)

        return [
            ChatResponse.model_validate(instance) for instance in res.scalars().all()
        ]

    async def count(
        self,
        **filters: Unpack[ChatGetListFilters],
    ) -> int:
        stmt = select(Chat)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = self._get_count_stmt(stmt)

        res = await self._session.execute(stmt)

        return res.scalar_one()
