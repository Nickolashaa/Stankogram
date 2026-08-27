from __future__ import annotations

from typing import TYPE_CHECKING, Any

from strawberry.permission import BasePermission

from ..context import AuthorizedAppInfo

if TYPE_CHECKING:
    from ..types.chats import Chat


class IsChatAdmin(BasePermission):
    message = "User is not chat admin"

    async def has_permission(
        self, source: Any, info: AuthorizedAppInfo, **kwargs: Any
    ) -> bool:
        if info.context.current_user.is_admin:
            return True

        try:
            chat_id: int = kwargs["input"].chat_id
        except KeyError:
            chat_id: int = kwargs["chat_id"]

        link = await info.context.services.chat_participant_service.get_or_none(
            chat_id=chat_id, user_id=info.context.current_user.id
        )
        if link is None:
            return False

        return link.is_admin


class IsChatParticipant(BasePermission):
    message = "User is not chat participant"

    async def has_permission(
        self, source: Chat | Any, info: AuthorizedAppInfo, **kwargs: Any
    ) -> bool:
        try:
            chat_id: int = kwargs["filters"].chat_id
        except KeyError:
            chat_id: int = source.id

        link = await info.context.services.chat_participant_service.get_or_none(
            chat_id=chat_id,
            user_id=info.context.current_user.id,
        )
        return link is not None
