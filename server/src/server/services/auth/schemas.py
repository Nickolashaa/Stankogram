from datetime import datetime
from typing import Literal, Self

import jwt
from pydantic import EmailStr, Field

from ...config import (
    JWT_ENCRYPTION_ALGORITHM,
    JWT_SECRET_KEY,
    PASSWORD_LEN,
)
from ...enums.users import Role
from ..base import BasePagination, BaseResponse, Schema


class JWTTokens(Schema):
    access_token: str
    refresh_token: str


class UserJWTPayload(Schema):
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
    role: Role
    is_admin: bool
    full_name: str


class UserCredentials(Schema):
    email: str
    password: str = Field(..., min_length=PASSWORD_LEN)


class PasswordResetRequest(Schema):
    email: EmailStr


class PasswordResetConfirm(Schema):
    id: int
    code: str


class UserInput(Schema):
    name: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    patronymic: str | None = Field(..., max_length=60)
    email: EmailStr
    role: Role
    is_admin: bool


class UserFilters(Schema):
    search_query: str | None = Field(None)
    role: Role | None = Field(None)
    is_admin: bool | None = Field(None)


class UserListQuery(UserFilters, BasePagination):
    pass
