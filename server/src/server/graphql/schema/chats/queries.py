import strawberry

from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAdmin, IsAuthenticated
from ...types.base import BasePaginationIn, default_pagination
from ...types.chats import (
    Chat,
    ChatFiltersIn,
    ChatsMeta,
)
from ...types.errors import UnauthorizedError


@strawberry.type
class ChatQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def me_chats(
        self,
        info: AuthorizedAppInfo,
        pagination: BasePaginationIn | None = None,
        filters: ChatFiltersIn | None = None,
    ) -> ChatsMeta | UnauthorizedError:
        links = await info.context.services.chat_participant_service.get_list(
            user_id=info.context.current_user.id,
        )

        return ChatsMeta(
            chats=[
                Chat.from_schema(instance)
                for instance in await info.context.services.chat_service.get_list(
                    pagination=(
                        pagination if pagination is not None else default_pagination
                    ).to_service_params(),
                    ids=[link.chat_id for link in links],
                    **filters.to_service_params() if filters is not None else {},
                )
            ],
            count=await info.context.services.chat_service.count(
                ids=[link.chat_id for link in links],
                **filters.to_service_params() if filters is not None else {},
            ),
        )

    @strawberry.field(permission_classes=[IsAdmin])
    async def chats(
        self,
        info: AuthorizedAppInfo,
        pagination: BasePaginationIn | None = None,
        filters: ChatFiltersIn | None = None,
    ) -> ChatsMeta:
        return ChatsMeta(
            chats=[
                Chat.from_schema(instance)
                for instance in await info.context.services.chat_service.get_list(
                    pagination=(
                        pagination if pagination is not None else default_pagination
                    ).to_service_params(),
                    **filters.to_service_params() if filters is not None else {},
                )
            ],
            count=await info.context.services.chat_service.count(
                **filters.to_service_params() if filters is not None else {},
            ),
        )
