from typing import NotRequired, Required, TypedDict


class SystemNotificationGetListFilters(TypedDict):
    unread_by_user_id: NotRequired[int]


class SystemNotificationCreateParams(TypedDict):
    text: Required[str]


class SystemNotificationUpdateParams(TypedDict):
    text: Required[str]
