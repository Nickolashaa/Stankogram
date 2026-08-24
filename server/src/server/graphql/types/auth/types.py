from typing import Self

import strawberry

from ....services.auth.schemas import JWTsSchema, UserResponse
from ..base import IBaseMeta, IBaseType
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
