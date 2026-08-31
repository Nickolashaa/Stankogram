import strawberry

from ....services.exceptions import ObjectAlreadyExists, ObjectNotFound
from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAdmin, IsAuthenticated
from ...types.errors import ObjectNotFoundError
from ...types.system_notifications import SystemNotification, SystemNotificationIn


@strawberry.type
class SystemNotificationMutation:
    @strawberry.mutation(permission_classes=[IsAdmin])
    async def create_system_notification(
        self,
        info: AuthorizedAppInfo,
        input: SystemNotificationIn,
    ) -> SystemNotification:
        instance = await info.context.services.system_notification_service.create(
            **input.to_create_service_params()
        )
        await info.context.session.commit()
        return SystemNotification.from_schema(instance)

    @strawberry.mutation(permission_classes=[IsAdmin])
    async def update_system_notification(
        self,
        info: AuthorizedAppInfo,
        id: int,
        input: SystemNotificationIn,
    ) -> SystemNotification | ObjectNotFoundError:
        try:
            instance = await info.context.services.system_notification_service.update(
                id=id, **input.to_update_service_params()
            )
            await info.context.session.commit()
            return SystemNotification.from_schema(instance)
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def mark_system_notification_read(
        self,
        info: AuthorizedAppInfo,
        id: int,
    ) -> None | ObjectNotFoundError:
        try:
            await info.context.services.system_notification_service.mark_as_read(
                id=id,
                user_id=info.context.current_user.id,
            )
            await info.context.session.commit()
        except ObjectAlreadyExists:
            await info.context.session.rollback()
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
