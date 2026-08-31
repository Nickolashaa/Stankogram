import strawberry

from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAdmin, IsAuthenticated
from ...types.base import BasePaginationIn, default_pagination
from ...types.system_notifications import (
    SystemNotification,
    SystemNotificationFiltersIn,
    SystemNotificationsMeta,
)


@strawberry.type
class SystemNotificationQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def me_system_notifications(
        self,
        info: AuthorizedAppInfo,
        pagination: BasePaginationIn | None = None,
        filters: SystemNotificationFiltersIn | None = None,
    ) -> SystemNotificationsMeta:
        service = info.context.services.system_notification_service
        params = (
            filters.to_service_params(info.context.current_user.id)
            if filters is not None
            else {}
        )

        return SystemNotificationsMeta(
            system_notifications=[
                SystemNotification.from_schema(instance)
                for instance in await service.get_list(
                    pagination=(
                        pagination if pagination is not None else default_pagination
                    ).to_service_params(),
                    **params,
                )
            ],
            count=await service.count(**params),
        )

    @strawberry.field(permission_classes=[IsAdmin])
    async def system_notifications(
        self,
        info: AuthorizedAppInfo,
        pagination: BasePaginationIn | None = None,
    ) -> SystemNotificationsMeta:
        service = info.context.services.system_notification_service

        return SystemNotificationsMeta(
            system_notifications=[
                SystemNotification.from_schema(instance)
                for instance in await service.get_list(
                    pagination=(
                        pagination if pagination is not None else default_pagination
                    ).to_service_params(),
                )
            ],
            count=await service.count(),
        )
