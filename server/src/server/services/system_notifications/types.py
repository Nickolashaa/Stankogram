from typing import NotRequired, Required, TypedDict


class SystemNotificationGetListFilters(TypedDict):
    unread_by_user_id: NotRequired[int]


class SystemNotificationCreateParams(TypedDict):
    title: Required[str]
    text: Required[str]


class SystemNotificationUpdateParams(TypedDict):
    title: Required[str]
    text: Required[str]
