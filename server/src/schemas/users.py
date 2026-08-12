from pydantic import EmailStr, Field

from ..config import (
    PASSWORD_LEN,
)
from ..enums.users import Role
from .base import BaseResponse, PaginationSchema, Schema


class UserResponse(BaseResponse):
    name: str
    surname: str
    patronymic: str | None
    email: str
    hashed_password: str
    role: Role
    is_admin: bool


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


class UserListQuery(UserFilters, PaginationSchema):
    pass
