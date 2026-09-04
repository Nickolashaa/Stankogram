from typing import Any

from strawberry.permission import BasePermission

from ...services.exceptions import ObjectNotFound
from ..context import AuthorizedAppInfo


class CanCreateMessage(BasePermission):
    message = "User can`t create message to this chat"

    async def has_permission(
        self, source: Any, info: AuthorizedAppInfo, **kwargs: Any
    ) -> bool:
        chat_id: int = kwargs["input"].chat_id

        link = await info.context.services.chat_participant_service.get_or_none(
            chat_id=chat_id,
            user_id=info.context.current_user.id,
        )

        if link is None:
            return False

        return not link.is_muted


class CanReactToMessage(BasePermission):
    message = "User can`t react to this message"

    async def has_permission(
        self, source: Any, info: AuthorizedAppInfo, **kwargs: Any
    ) -> bool:
        message_id: int = kwargs["input"].message_id

        try:
            instance = await info.context.services.message_service.get(message_id)
        except ObjectNotFound:
            return False

        link = await info.context.services.chat_participant_service.get_or_none(
            chat_id=instance.chat_id,
            user_id=info.context.current_user.id,
        )

        if link is None:
            return False

        return not link.is_muted
