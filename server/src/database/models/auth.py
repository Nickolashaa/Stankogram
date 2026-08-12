from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from ...enums.users import Role
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

    role: Mapped[Role]
    is_admin: Mapped[bool] = mapped_column(
        server_default=expression.false(),
    )


class PasswordResetCode(Base):
    __tablename__ = "password_reset_codes"

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    value: Mapped[str]
