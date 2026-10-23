from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from ...enums.users import UserRole
from ..connection import Base


class CancelledToken(Base):
    __tablename__ = "cancelled_tokens"

    jti: Mapped[UUID] = mapped_column(unique=True)


class User(Base):
    __tablename__ = "users"

    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str | None]

    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    role: Mapped[UserRole]
    is_admin: Mapped[bool] = mapped_column(
        server_default=expression.false(),
    )

    last_online_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    @hybrid_property
    def full_name(self) -> str:
        return f"{self.surname} {self.name} {self.patronymic or ''}".strip()

    @full_name.expression
    def full_name(cls):
        return func.trim(
            cls.surname + " " + cls.name + " " + func.coalesce(cls.patronymic, "")
        )
