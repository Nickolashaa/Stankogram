from typing import Unpack

from sqlalchemy import insert, select, Select
from sqlalchemy.exc import IntegrityError

from ...database.models.chats import Chat

from ...enums.chats import ChatType
from ..exceptions import InvalidInput, ObjectNotFound
from .schemas import ChatResponse
from ..base import BaseService, BasePagination
from .types import ChatCreateParams, ChatGetListFilters


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

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[ChatResponse]],
        **filters: Unpack[ChatGetListFilters],
    ) -> Select[tuple[ChatResponse]]:
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
        stmt = select(Chat)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        res = await self._session.execute(stmt)

        return [
            ChatResponse.model_validate(instance)
            for instance in res.scalars().all()
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
