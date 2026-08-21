from datetime import datetime
from typing import Literal, Self

import jwt

from ...config import (
    JWT_ENCRYPTION_ALGORITHM,
    JWT_SECRET_KEY,
)
from ...enums.users import UserRole
from ..base import BaseResponse, Schema


class JWTsSchema(Schema):
    access_token: str
    refresh_token: str


class JWTPayload(Schema):
    id: int
    is_admin: bool
    jti: str
    type: Literal["refresh", "access"]
    exp: datetime

    def generate_token(self) -> str:
        return jwt.encode(
            payload=self.model_dump(),
            key=JWT_SECRET_KEY,
            algorithm=JWT_ENCRYPTION_ALGORITHM,
        )

    @classmethod
    def from_token(cls, token: str) -> Self:
        return cls.model_validate(
            jwt.decode(
                jwt=token, key=JWT_SECRET_KEY, algorithms=[JWT_ENCRYPTION_ALGORITHM]
            )
        )


class UserResponse(BaseResponse):
    name: str
    surname: str
    patronymic: str | None
    email: str
    hashed_password: str
    role: UserRole
    is_admin: bool
    full_name: str
