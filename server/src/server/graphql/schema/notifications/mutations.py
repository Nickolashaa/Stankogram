import strawberry

from ....services.exceptions import ObjectNotFound
from ...context import AuthorizedAppInfo
from ...permissions.auth import IsAuthenticated
from ...types.errors import ObjectNotFoundError


@strawberry.type
class NotificationMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def hide_notification(
        self,
        info: AuthorizedAppInfo,
        id: int,
    ) -> None | ObjectNotFoundError:
        try:
            await info.context.services.notification_service.hide(
                id=id,
                user_id=info.context.current_user.id,
            )
            await info.context.session.commit()
        except ObjectNotFound as e:
            await info.context.session.rollback()
            return ObjectNotFoundError.from_service_exception(e)
