from pydantic import Field

from ..config import (
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
    is_admin: bool


class UserFilters(Schema):
    search_query: str | None = Field(None)
    role: Role | None = Field(None)
    is_admin: bool | None = Field(None)
