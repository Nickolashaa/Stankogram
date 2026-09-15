from typing import Self

import strawberry

from ....services.notifications.schemas import NotificationResponse
from ..base import IBaseMeta, IBaseType
from ..messages.interfaces import IMessage


@strawberry.type
class Notification(IBaseType, IMessage):
    is_hidden: bool

    @classmethod
    def from_schema(cls, instance: NotificationResponse) -> Self:
        return cls(
            id=instance.id,
            message_id=instance.message_id,
            is_hidden=instance.is_hidden,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )


@strawberry.type
class NotificationsMeta(IBaseMeta):
    notifications: list[Notification]
