from sqlalchemy import Select, delete, insert, select
from sqlalchemy.exc import IntegrityError

from ..database.models.users_to_chats import UsersToChats
from ..schemas.base import PaginationSchema
from ..schemas.users_to_chats import (
    UsersToChatsFilters,
    UsersToChatsInput,
    UsersToChatsResponse,
)
from .base import BaseService
from .exceptions import ObjectAlreadyExists, ObjectNotFound


class UsersToChatsService(BaseService):
    async def create(
        self,
        data: UsersToChatsInput,
    ) -> UsersToChatsResponse:
        stmt = insert(UsersToChats).values(**data.model_dump()).returning(UsersToChats)

        try:
            res = await self._session.execute(stmt)
        except IntegrityError as e:
            error_text = str(e.orig)
            if "uq_user_chat" in error_text:
                raise ObjectAlreadyExists("User already in this chat")
            if "fk_users_to_chats_user_id" in error_text:
                raise ObjectNotFound(f"User with id {data.user_id} not found")
            if "fk_users_to_chats_chat_id" in error_text:
                raise ObjectNotFound(f"Chat with id {data.chat_id} not found")

        return UsersToChatsResponse.model_validate(res.scalar_one())

    async def delete(
        self,
        data: UsersToChatsInput,
    ) -> None:
        stmt = delete(UsersToChats).where(
            UsersToChats.user_id == data.user_id,
            UsersToChats.chat_id == data.chat_id,
        )
        await self._session.execute(stmt)

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[UsersToChats]],
        filters: UsersToChatsFilters | None,
    ) -> Select[tuple[UsersToChats]]:
        if filters is None:
            return stmt

        if "chat_id" in filters.model_fields_set:
            stmt = stmt.where(UsersToChats.chat_id == filters.chat_id)

        if "user_id" in filters.model_fields_set:
            stmt = stmt.where(UsersToChats.user_id == filters.user_id)

        return stmt

    async def get_list(
        self,
        filters: UsersToChatsFilters | None = None,
        pagination: PaginationSchema | None = None,
    ) -> list[UsersToChatsResponse]:
        stmt = select(UsersToChats)

        stmt = self._apply_filters(stmt=stmt, filters=filters)

        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)

        res = await self._session.execute(stmt)

        return [
            UsersToChatsResponse.model_validate(entity)
            for entity in res.scalars().all()
        ]
