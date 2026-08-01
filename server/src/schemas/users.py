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
