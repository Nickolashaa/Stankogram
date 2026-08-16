from typing import Iterable, Unpack

from cryptography.fernet import Fernet
from sqlalchemy import Select, delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models.messages import Message
from ...exceptions import Forbidden, ObjectNotFound
from ...schemas.messages import MessageResponse
from ...utils.stmt_modificators import _get_count_stmt
from ..base import BaseService
from ..chats import ChatService
from .types import MessageCreateParams, MessageGetListFilters


class MessageService(BaseService):
    def __init__(
        self, session: AsyncSession, fernet: Fernet, chat_service: ChatService
    ):
        super().__init__(session)
        self._fernet = fernet
        self._chat_service = chat_service

    async def _can_message_to_chat(
        self,
        chat_id: int,
        user_id: int,
    ) -> bool:
        return await self._chat_service.is_exists(
            user_id=user_id,
            chat_id=chat_id,
        )

    async def create(
        self,
        **values: Unpack[MessageCreateParams],
    ) -> MessageResponse:
        if (
            await self._can_message_to_chat(
                chat_id=values.get("chat_id"),
                user_id=values.get("user_id"),
            )
            is False
        ):
            raise Forbidden("Dont have access to this chat.")

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

        if (ids := filters.get("ids")) is not None:
            stmt = stmt.where(Message.id.in_(ids))

        return stmt

    async def get_list(
        self,
        limit: int | None,
        offset: int | None,
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
                user_id=entity.user_id,
                type=entity.type,
                text=self._fernet.decrypt(entity.encrypted_text.encode()).decode(),
                created_at=entity.created_at,
                updated_at=entity.updated_at,
            )
            for entity in res.scalars().all()
        ]

    async def load(
        self,
        ids: Iterable[int],
    ) -> dict[int, MessageResponse]:
        return {
            entity.id: entity
            for entity in await self.get_list(
                limit=None,
                offset=None,
                ids=ids,
            )
        }

    async def count(
        self,
        **filters: Unpack[MessageGetListFilters],
    ) -> int:
        stmt = select(Message)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = _get_count_stmt(stmt)

        res = await self._session.execute(stmt)

        return res.scalar_one()
