from typing import Self

import strawberry

from ....services.system_notifications.schemas import SystemNotificationResponse
from ..base import IBaseMeta, IBaseType


@strawberry.type
class SystemNotification(IBaseType):
    title: str
    text: str

    @classmethod
    def from_schema(cls, instance: SystemNotificationResponse) -> Self:
        return cls(
            id=instance.id,
            title=instance.title,
            text=instance.text,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )


@strawberry.type
class SystemNotificationsMeta(IBaseMeta):
    system_notifications: list[SystemNotification]
