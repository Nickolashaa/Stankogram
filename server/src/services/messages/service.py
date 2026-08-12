from typing import Unpack

from cryptography.fernet import Fernet
from sqlalchemy import Select, delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models.messages import Message
from ...schemas.messages import MessageResponse
from ...utils.stmt_modificators import _get_count_stmt
from ..base import BaseService
from ..exceptions import ObjectNotFound
from .types import MessageCreateParams, MessageGetListFilters


class MessageService(BaseService):
    def __init__(self, session: AsyncSession, fernet: Fernet):
        super().__init__(session)
        self._fernet = fernet

    async def create(
        self,
        **values: Unpack[MessageCreateParams],
    ) -> MessageResponse:
        stmt = (
            insert(Message)
            .values(
                chat_id=values["chat_id"],
                type=values["type"],
                encrypted_text=self._fernet.encrypt(values["text"].encode()).decode(),
            )
            .returning(Message)
        )
        try:
            res = await self._session.execute(stmt)
        except IntegrityError:
            raise ObjectNotFound(f"Chat with id {values['chat_id']} not found")

        return MessageResponse.model_validate(res.scalar_one())

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

        if (type_ := filters.get("type")) is not None:
            stmt = stmt.where(Message.type == type_)

        return stmt

    async def get_list(
        self,
        limit: int,
        offset: int,
        **filters: Unpack[MessageGetListFilters],
    ) -> list[MessageResponse]:
        stmt = select(Message).order_by(Message.created_at.desc())

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = stmt.limit(limit).offset(offset)

        res = await self._session.execute(stmt)

        return [
            MessageResponse(
                id=entity.id,
                chat_id=entity.chat_id,
                type=entity.type,
                text=self._fernet.decrypt(entity.encrypted_text.encode()).decode(),
                created_at=entity.created_at,
                updated_at=entity.updated_at,
            )
            for entity in res.scalars().all()
        ]

    async def count(
        self,
        **filters: Unpack[MessageGetListFilters],
    ) -> int:
        stmt = select(Message)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = _get_count_stmt(stmt)

        res = await self._session.execute(stmt)

        return res.scalar_one()
