import strawberry

from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAuthenticated
from ...permissions.chats import IsChatParticipant
from ...types.base import BasePaginationIn, default_pagination
from ...types.messages import Message, MessageFiltersIn, MessagesMeta


@strawberry.type
class MessageQuery:
    @strawberry.field(permission_classes=[IsAuthenticated, IsChatParticipant])
    async def messages(
        self,
        info: AuthorizedAppInfo,
        filters: MessageFiltersIn,
        pagination: BasePaginationIn | None = None,
    ) -> MessagesMeta:
        return MessagesMeta(
            messages=[
                Message.from_schema(instance)
                for instance in await info.context.services.message_service.get_list(
                    pagination=(
                        pagination if pagination is not None else default_pagination
                    ).to_service_params(),
                    **filters.to_service_params(),
                )
            ],
            count=await info.context.services.message_service.count(
                **filters.to_service_params(),
            ),
        )
