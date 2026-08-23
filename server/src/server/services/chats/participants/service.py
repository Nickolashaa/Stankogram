from typing import Unpack

from sqlalchemy import Select, delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ....database.models.chats import ChatParticipant
from ....enums.chats import ChatType
from ...base import BasePagination, BaseService
from ...exceptions import InvalidInput, ObjectAlreadyExists, ObjectNotFound
from ..service import ChatService
from .schemas import ChatParticipantResponse
from .types import (
    ChatParticipantCreateParams,
    ChatParticipantGetListFilters,
)


class ChatParticipantService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        chat_service: ChatService,
    ) -> None:
        super().__init__(session)
        self._chat_service = chat_service

    async def create(
        self,
        **data: Unpack[ChatParticipantCreateParams],
    ) -> ChatParticipantResponse:
        chat = await self._chat_service.get(data.get("chat_id"))
        if chat.type == ChatType.PRIVATE:
            participants_count = await self.count(chat_id=chat.id)
            if participants_count >= 2:
                raise InvalidInput(
                    "You cannot change the participants of a private chat"
                )

        stmt = insert(ChatParticipant).values(**data).returning(ChatParticipant)

        try:
            res = await self._session.execute(stmt)
        except IntegrityError as e:
            if "uq_user_chat" in str(e.orig):
                raise ObjectAlreadyExists("User already exists in this chat")
            if "fk_chat_participants_user_id" in str(e.orig):
                raise ObjectNotFound(f"User with id {data.get('user_id')} not found")
            raise

        return ChatParticipantResponse.model_validate(res.scalar_one())

    async def delete(
        self,
        chat_id: int,
        user_id: int,
    ) -> None:
        chat = await self._chat_service.get(chat_id)
        if chat.type == ChatType.PRIVATE:
            raise InvalidInput("You cannot change the participants of a private chat")

        stmt = delete(ChatParticipant).where(
            ChatParticipant.chat_id == chat_id, ChatParticipant.user_id == user_id
        )
        await self._session.execute(stmt)

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[ChatParticipant]],
        **filters: Unpack[ChatParticipantGetListFilters],
    ) -> Select[tuple[ChatParticipant]]:
        if (chat_id := filters.get("chat_id")) is not None:
            stmt = stmt.where(ChatParticipant.chat_id == chat_id)

        if (user_id := filters.get("user_id")) is not None:
            stmt = stmt.where(ChatParticipant.user_id == user_id)

        if (exclude_user_ids := filters.get("exclude_user_ids")) is not None:
            stmt = stmt.where(ChatParticipant.user_id.not_in(exclude_user_ids))

        return stmt

    async def get_list(
        self,
        pagination: BasePagination | None = None,
        **filters: Unpack[ChatParticipantGetListFilters],
    ) -> list[ChatParticipantResponse]:
        stmt = select(ChatParticipant)

        stmt = self._apply_filters(stmt, **filters)

        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        res = await self._session.execute(stmt)

        return [
            ChatParticipantResponse.model_validate(entity)
            for entity in res.scalars().all()
        ]

    async def count(
        self,
        **filters: Unpack[ChatParticipantGetListFilters],
    ) -> int:
        stmt = select(ChatParticipant)

        stmt = self._apply_filters(stmt, **filters)

        stmt = self._get_count_stmt(stmt)

        res = await self._session.execute(stmt)

        return res.scalar_one()
