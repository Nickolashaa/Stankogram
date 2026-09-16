from datetime import UTC, datetime, timedelta
from typing import Self

import strawberry

from ....config import PRESENCE_RECENTLY_HOURS
from ....services.auth.schemas import (
    CreatedUserSchema,
    JWTsSchema,
    UserResponse,
    UsersImportReportSchema,
)
from ...pubsub import pub_sub
from ..base import IBaseMeta, IBaseType, XlsxFile
from .enums import EUserOnlineStatus, EUserRole


@strawberry.type
class User(IBaseType):
    id: int
    name: str
    surname: str
    patronymic: str | None
    email: str
    role: EUserRole
    is_admin: bool
    full_name: str
    online_status: EUserOnlineStatus
    last_online_at: datetime | None
    hide_last_online: bool

    @staticmethod
    def _compile_online_status(instance: UserResponse) -> EUserOnlineStatus:
        if pub_sub.is_exists(instance.id) is True:
            return EUserOnlineStatus.ONLINE

        if instance.last_online_at is None:
            return EUserOnlineStatus.LONG_AGO

        if (
            datetime.now(UTC) - timedelta(hours=PRESENCE_RECENTLY_HOURS)
            < instance.last_online_at
        ):
            return EUserOnlineStatus.RECENTLY_ONLINE

        return EUserOnlineStatus.LONG_AGO

    @classmethod
    def from_schema(
        cls,
        instance: UserResponse,
    ) -> Self:
        return cls(
            id=instance.id,
            name=instance.name,
            surname=instance.surname,
            patronymic=instance.patronymic,
            email=instance.email,
            role=instance.role,
            is_admin=instance.is_admin,
            full_name=instance.full_name,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
            hide_last_online=instance.hide_last_online,
            online_status=cls._compile_online_status(instance),
            last_online_at=(
                None if instance.hide_last_online else instance.last_online_at
            ),
        )


@strawberry.type
class CreatedUser:
    user: User
    password: str

    @classmethod
    def from_schema(cls, instance: CreatedUserSchema) -> Self:
        return cls(
            user=User.from_schema(instance.user),
            password=instance.password,
        )


@strawberry.type
class JWTs:
    access_token: str
    refresh_token: str

    @classmethod
    def from_schema(
        cls,
        instance: JWTsSchema,
    ) -> Self:
        return cls(
            access_token=instance.access_token,
            refresh_token=instance.refresh_token,
        )


@strawberry.type
class UsersMeta(IBaseMeta):
    users: list[User]


@strawberry.type
class UsersImportReport:
    file: XlsxFile
    total: int
    succeeded: int
    failed: int

    @classmethod
    def from_schema(cls, instance: UsersImportReportSchema) -> Self:
        return cls(
            file=XlsxFile.from_schema(instance.file),
            total=instance.total,
            succeeded=instance.succeeded,
            failed=instance.failed,
        )
