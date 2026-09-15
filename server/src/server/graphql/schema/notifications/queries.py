import strawberry

from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAuthenticated
from ...types.base import BasePaginationIn, default_pagination
from ...types.notifications import Notification, NotificationsMeta


@strawberry.type
class NotificationQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def me_notifications(
        self,
        info: AuthorizedAppInfo,
        pagination: BasePaginationIn | None = None,
    ) -> NotificationsMeta:
        service = info.context.services.notification_service
        filters = {"user_id": info.context.current_user.id, "only_visible": True}

        return NotificationsMeta(
            notifications=[
                Notification.from_schema(instance)
                for instance in await service.get_list(
                    pagination=(
                        pagination if pagination is not None else default_pagination
                    ).to_service_params(),
                    **filters,
                )
            ],
            count=await service.count(**filters),
        )
