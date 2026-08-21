from typing import Self

import strawberry

from ....services.auth.schemas import UserResponse
from .enums import EUserRole


@strawberry.type
class User:
    id: int
    name: str
    surname: str
    patronymic: str | None
    email: str
    hashed_password: str
    role: EUserRole
    is_admin: bool

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
            hashed_password=instance.hashed_password,
            role=instance.role,
            is_admin=instance.is_admin,
        )
