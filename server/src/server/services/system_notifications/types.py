from datetime import datetime
from typing import NotRequired, Required, TypedDict


class SystemNotificationGetListFilters(TypedDict):
    unread_by_user_id: NotRequired[int]
    only_active: NotRequired[bool]


class SystemNotificationCreateParams(TypedDict):
    title: Required[str]
    text: Required[str]
    expires_at: NotRequired[datetime | None]


class SystemNotificationUpdateParams(TypedDict):
    title: Required[str]
    text: Required[str]
    expires_at: Required[datetime | None]
