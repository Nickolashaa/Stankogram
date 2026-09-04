from typing import Unpack

from cryptography.fernet import Fernet
from sqlalchemy import Select, delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models.messages import Message
from ..base import BasePagination, BaseService
from ..exceptions import ObjectNotFound
from .schemas import MessageResponse
from .types import MessageCreateParams, MessageGetListFilters


class MessageService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        fernet: Fernet,
    ):
        super().__init__(session)
        self._fernet = fernet

    async def create(
        self,
        **values: Unpack[MessageCreateParams],
    ) -> MessageResponse:
        stmt = (
            insert(Message)
            .values(
                chat_id=values.get("chat_id"),
                user_id=values.get("user_id"),
                type=values.get("type"),
                encrypted_text=self._fernet.encrypt(
                    values.get("text").encode()
                ).decode(),
            )
            .returning(Message)
        )
        try:
            res = await self._session.execute(stmt)
        except IntegrityError as e:
            if "fk_messages_chat_id" in str(e.orig):
                raise ObjectNotFound(f"Chat with id {values.get('chat_id')} not found")
            if "fk_messages_user_id" in str(e.orig):
                raise ObjectNotFound(f"User with id {values.get('user_id')} not found")
            raise

        return MessageResponse.from_ORM(fernet=self._fernet, instance=res.scalar_one())

    async def delete(self, id: int) -> None:
        stmt = delete(Message).where(Message.id == id)
        await self._session.execute(stmt)

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[Message]],
        **filters: Unpack[MessageGetListFilters],
    ) -> Select[tuple[Message]]:
        if (chat_id := filters.get("chat_id")) is not None:
            stmt = stmt.where(Message.chat_id == chat_id)

        if (chat_ids := filters.get("chat_ids")) is not None:
            stmt = stmt.where(Message.chat_id.in_(chat_ids))

        return stmt

    async def get_list(
        self,
        pagination: BasePagination | None = None,
        **filters: Unpack[MessageGetListFilters],
    ) -> list[MessageResponse]:
        stmt = select(Message).order_by(Message.created_at.desc())

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        res = await self._session.execute(stmt)

        return [
            MessageResponse.from_ORM(fernet=self._fernet, instance=entity)
            for entity in res.scalars().all()
        ]

    async def count(
        self,
        **filters: Unpack[MessageGetListFilters],
    ) -> int:
        stmt = select(Message)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = self._get_count_stmt(stmt)

        res = await self._session.execute(stmt)

        return res.scalar_one()
