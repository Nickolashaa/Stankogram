from typing import NotRequired, TypedDict


class NotificationGetListFilters(TypedDict):
    user_id: NotRequired[int]
    message_id: NotRequired[int]
    only_visible: NotRequired[bool]
