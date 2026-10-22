from datetime import datetime
from typing import Self

import strawberry

from ....services.auth.schemas import (
    CreatedUserSchema,
    JWTsSchema,
    UserResponse,
    UsersImportReportSchema,
)
from ...context import AppInfo
from ..base import IBaseMeta, IBaseType, XlsxFile
from .enums import EUserRole


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
    last_online_at: datetime | None

    @strawberry.field
    async def is_online(self, info: AppInfo) -> bool:
        return await info.context.data_loaders.presence_loader.load(self.id)

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
            last_online_at=instance.last_online_at,
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
