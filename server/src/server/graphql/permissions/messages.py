from typing import Any

from strawberry.permission import BasePermission

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


class IsMessageAuthor(BasePermission):
    message = "User is not the author of this message"

    async def has_permission(
        self, source: Any, info: AuthorizedAppInfo, **kwargs: Any
    ) -> bool:
        if info.context.current_user.is_admin:
            return True

        message_id: int = kwargs["message_id"]

        message = await info.context.services.message_service.get_or_none(message_id)
        if message is None:
            return False

        return message.user_id == info.context.current_user.id


class CanDeleteMessage(BasePermission):
    message = "User can`t delete this message"

    async def has_permission(
        self, source: Any, info: AuthorizedAppInfo, **kwargs: Any
    ) -> bool:
        if info.context.current_user.is_admin:
            return True

        message_id: int = kwargs["message_id"]

        message = await info.context.services.message_service.get_or_none(message_id)
        if message is None:
            return False

        if message.user_id == info.context.current_user.id:
            return True

        link = await info.context.services.chat_participant_service.get_or_none(
            chat_id=message.chat_id,
            user_id=info.context.current_user.id,
        )
        if link is None:
            return False

        return link.is_admin


class CanReadMessage(BasePermission):
    message = "User can`t read this message"

    async def has_permission(
        self, source: Any, info: AuthorizedAppInfo, **kwargs: Any
    ) -> bool:
        message_id: int = kwargs["message_id"]

        message = await info.context.services.message_service.get_or_none(message_id)
        if message is None:
            return False

        link = await info.context.services.chat_participant_service.get_or_none(
            chat_id=message.chat_id,
            user_id=info.context.current_user.id,
        )

        return link is not None
