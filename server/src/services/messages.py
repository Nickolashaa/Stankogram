from cryptography.fernet import Fernet
from sqlalchemy import Select, delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models.messages import Message
from ..schemas.base import PaginationSchema
from ..schemas.messages import MessageCreate, MessageFilters, MessageResponse
from .base import BaseService
from .exceptions import ObjectNotFound


class MessagesService(BaseService):
    def __init__(self, session: AsyncSession, fernet: Fernet):
        super().__init__(session)
        self._fernet = fernet

    async def create(self, data: MessageCreate) -> MessageResponse:
        stmt = (
            insert(Message)
            .values(
                chat_id=data.chat_id,
                type=data.type,
                encrypted_text=self._fernet.encrypt(data.text.encode()).decode(),
            )
            .returning(Message)
        )
        try:
            res = await self._session.execute(stmt)
        except IntegrityError:
            raise ObjectNotFound(f"Chat with id {data.chat_id} not found")

        return MessageResponse.model_validate(res.scalar_one())

    async def delete(self, id: int) -> None:
        stmt = delete(Message).where(Message.id == id)
        await self._session.execute(stmt)

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[Message]],
        filters: MessageFilters | None,
    ) -> Select[tuple[Message]]:
        if filters is None:
            return stmt

        if "chat_id" in filters.model_fields_set:
            stmt = stmt.where(Message.chat_id == filters.chat_id)

        if "type" in filters.model_fields_set:
            stmt = stmt.where(Message.type == filters.type)

        return stmt

    async def get_list(
        self,
        filters: MessageFilters | None,
        pagination: PaginationSchema | None,
    ) -> list[MessageResponse]:
        stmt = select(Message).order_by(Message.created_at.desc())

        stmt = self._apply_filters(stmt=stmt, filters=filters)

        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        res = await self._session.execute(stmt)
        entities = res.scalars().all()

        return [
            MessageResponse(
                id=entity.id,
                chat_id=entity.chat_id,
                type=entity.type,
                text=self._fernet.decrypt(entity.encrypted_text.encode()).decode(),
                created_at=entity.created_at,
                updated_at=entity.updated_at,
            )
            for entity in entities
        ]
