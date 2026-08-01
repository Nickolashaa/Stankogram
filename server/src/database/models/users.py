from ..connection import Base
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum
from sqlalchemy.sql import expression
from ..mixins.timestamp import TimestampMixin


class UserType(Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str | None]
    login: Mapped[str]
    hashed_password: Mapped[str]
    type: Mapped[UserType]
    is_admin: Mapped[bool] = mapped_column(
        server_default=expression.false(),
    )
