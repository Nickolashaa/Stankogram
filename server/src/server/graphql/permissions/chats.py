from typing import Any

from strawberry.permission import BasePermission

from ..context import AuthorizedAppInfo


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
