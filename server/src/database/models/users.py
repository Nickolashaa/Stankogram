from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from ..connection import Base


class UserType(Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class User(Base):
    __tablename__ = "users"

    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str | None]
    login: Mapped[str]
    hashed_password: Mapped[str]
    type: Mapped[UserType]
    is_admin: Mapped[bool] = mapped_column(
        server_default=expression.false(),
    )
