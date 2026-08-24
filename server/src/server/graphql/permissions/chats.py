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
        try:
            chat_id: int = kwargs["input"].chat_id
        except KeyError:
            chat_id: int = kwargs["chat_id"]

        links = await info.context.services.chat_participant_service.get_list(
            chat_id=chat_id, user_id=info.context.current_user.id
        )
        if not links:
            return False

        return links[0].is_admin


class IsChatParticipant(BasePermission):
    message = "User is not chat participant"

    async def has_permission(
        self, source: Chat | Any, info: AuthorizedAppInfo, **kwargs: Any
    ) -> bool:
        try:
            chat_id: int = kwargs["filters"].chat_id
        except KeyError:
            chat_id: int = source.id

        links = await info.context.services.chat_participant_service.get_list(
            chat_id=chat_id,
            user_id=info.context.current_user.id,
        )
        return len(links) > 0
