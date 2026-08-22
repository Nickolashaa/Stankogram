import strawberry

from ...context import AppInfo
from ...permissions.auth import IsAdmin, IsAuthenticated
from ...types.base import BasePaginationIn, default_pagination
from ...types.chats import (
    Chat,
    ChatFiltersIn,
    ChatParticipant,
    ChatParticipantFiltersIn,
)
from ...types.errors import UnauthorizedError


@strawberry.type
class ChatQuery:
    @strawberry.field(permission_classes=[IsAdmin])
    async def chats_participants(
        self,
        info: AppInfo,
        pagination: BasePaginationIn | None = None,
        filters: ChatParticipantFiltersIn | None = None,
    ) -> list[ChatParticipant]:
        return [
            ChatParticipant.from_schema(instance)
            for instance in await info.context.services.chat_participant_service.get_list(  # noqa: E501
                pagination=(
                    pagination if pagination is not None else default_pagination
                ).to_service_params(),
                **filters.to_service_params() if filters is not None else {},
            )
        ]

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def me_chats(
        self,
        info: AppInfo,
        pagination: BasePaginationIn | None = None,
        filters: ChatFiltersIn | None = None,
    ) -> list[Chat] | UnauthorizedError:
        if info.context.current_user is None:
            return UnauthorizedError(message="User not authorized")

        links = await info.context.services.chat_participant_service.get_list(
            user_id=info.context.current_user.id,
        )

        return [
            Chat.from_schema(instance)
            for instance in await info.context.services.chat_service.get_list(
                pagination=(
                    pagination if pagination is not None else default_pagination
                ).to_service_params(),
                ids=[link.chat_id for link in links],
                **filters.to_service_params() if filters is not None else {},
            )
        ]

    @strawberry.field(permission_classes=[IsAdmin])
    async def chats(
        self,
        info: AppInfo,
        pagination: BasePaginationIn | None = None,
        filters: ChatFiltersIn | None = None,
    ) -> list[Chat]:
        return [
            Chat.from_schema(instance)
            for instance in await info.context.services.chat_service.get_list(
                pagination=(
                    pagination if pagination is not None else default_pagination
                ).to_service_params(),
                **filters.to_service_params() if filters is not None else {},
            )
        ]
