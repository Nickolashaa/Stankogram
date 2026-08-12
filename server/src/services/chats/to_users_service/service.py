from typing import Unpack

from sqlalchemy import Select, delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import aliased

from ....database.models.chats_to_users import ChatToUser
from ....schemas.chats_to_users import ChatToUserResponse
from ....utils.stmt_modificators import _get_count_stmt
from ...base import BaseService
from ...exceptions import ObjectAlreadyExists, ObjectNotFound
from .types import ChatToUserGetListFilters, ChatToUserParams


class ChatToUserService(BaseService):
    async def get_by_participants(
        self,
        first_user_id: int,
        second_user_id: int,
    ) -> ChatToUserResponse:
        first_membership = aliased(ChatToUser)
        second_membership = aliased(ChatToUser)

        stmt = (
            select(first_membership)
            .join(
                second_membership,
                second_membership.chat_id == first_membership.chat_id,
            )
            .where(
                first_membership.user_id == first_user_id,
                second_membership.user_id == second_user_id,
            )
        )

        res = await self._session.execute(stmt)

        entity = res.scalar_one_or_none()
        if entity is None:
            raise ObjectNotFound(
                f"Private chat between users {first_user_id} and "
                f"{second_user_id} not found"
            )

        return ChatToUserResponse.model_validate(entity)

    async def create(
        self,
        **values: Unpack[ChatToUserParams],
    ) -> ChatToUserResponse:
        stmt = insert(ChatToUser).values(**values).returning(ChatToUser)

        try:
            res = await self._session.execute(stmt)
        except IntegrityError as e:
            error_text = str(e.orig)
            if "uq_user_chat" in error_text:
                raise ObjectAlreadyExists("User already in this chat")
            if "fk_users_to_chats_user_id" in error_text:
                raise ObjectNotFound(f"User with id {values['user_id']} not found")
            if "fk_users_to_chats_chat_id" in error_text:
                raise ObjectNotFound(f"Chat with id {values['chat_id']} not found")

        return ChatToUserResponse.model_validate(res.scalar_one())

    async def delete(
        self,
        **values: Unpack[ChatToUserParams],
    ) -> None:
        stmt = delete(ChatToUser).where(
            ChatToUser.user_id == values["user_id"],
            ChatToUser.chat_id == values["chat_id"],
        )
        await self._session.execute(stmt)

    @staticmethod
    def _apply_filters(
        stmt: Select[tuple[ChatToUser]],
        **filters: Unpack[ChatToUserGetListFilters],
    ) -> Select[tuple[ChatToUser]]:
        if (chat_id := filters.get("chat_id")) is not None:
            stmt = stmt.where(ChatToUser.chat_id == chat_id)

        if (user_id := filters.get("user_id")) is not None:
            stmt = stmt.where(ChatToUser.user_id == user_id)

        return stmt

    async def get_list(
        self,
        limit: int,
        offset: int,
        **filters: Unpack[ChatToUserGetListFilters],
    ) -> list[ChatToUserResponse]:
        stmt = select(ChatToUser)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = stmt.limit(limit).offset(offset)

        res = await self._session.execute(stmt)

        return [
            ChatToUserResponse.model_validate(entity) for entity in res.scalars().all()
        ]

    async def count(
        self,
        **filters: Unpack[ChatToUserGetListFilters],
    ) -> int:
        stmt = select(ChatToUser)

        stmt = self._apply_filters(stmt=stmt, **filters)

        stmt = _get_count_stmt(stmt)

        res = await self._session.execute(stmt)

        return res.scalar_one()
