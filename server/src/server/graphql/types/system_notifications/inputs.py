import strawberry

from ....services.system_notifications.types import (
    SystemNotificationCreateParams,
    SystemNotificationGetListFilters,
    SystemNotificationUpdateParams,
)


@strawberry.input
class SystemNotificationFiltersIn:
    only_unread: strawberry.Maybe[bool]

    def to_service_params(
        self,
        current_user_id: int,
    ) -> SystemNotificationGetListFilters:
        params: SystemNotificationGetListFilters = {}

        if self.only_unread is not None and self.only_unread.value:
            params["unread_by_user_id"] = current_user_id

        return params


@strawberry.input
class SystemNotificationIn:
    text: str

    def to_create_service_params(self) -> SystemNotificationCreateParams:
        return SystemNotificationCreateParams(text=self.text)

    def to_update_service_params(self) -> SystemNotificationUpdateParams:
        return SystemNotificationUpdateParams(text=self.text)
