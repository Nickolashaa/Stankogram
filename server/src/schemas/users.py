from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import jwt
from pydantic import Field

from ..config import (
    JWT_ACCESS_EXP_MINUTES,
    JWT_ENCRYPTION_ALGORITHM,
    JWT_REFRESH_EXP_DAYS,
    JWT_SECRET_KEY,
    MIN_PASSWORD_LEN,
)
from ..enums.users import Role
from .base import Schema


class UserResponse(Schema):
    id: int
    name: str
    surname: str
    patronymic: str | None
    login: str
    hashed_password: str
    role: Role
    is_admin: bool


class UserCredentials(Schema):
    login: str
    password: str = Field(..., min_length=MIN_PASSWORD_LEN)


class UserCreate(Schema):
    name: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    patronymic: str | None = Field(..., max_length=60)
    phone_number: str = Field(..., min_length=12, max_length=12)
    role: Role


class UserJWTPayload(Schema):
    id: int
    is_admin: bool
    jti: UUID = Field(default=uuid4())

    def generate_token(self) -> str:
        return jwt.encode(
            payload=self.model_dump(),
            key=JWT_SECRET_KEY,
            algorithm=JWT_ENCRYPTION_ALGORITHM,
        )


class UserJWTAccessPayload(UserJWTPayload):
    exp: datetime = Field(
        default=datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_EXP_MINUTES)
    )


class UserJWTRefreshPayload(UserJWTPayload):
    exp: datetime = Field(
        default=datetime.now(timezone.utc) + timedelta(days=JWT_REFRESH_EXP_DAYS)
    )
