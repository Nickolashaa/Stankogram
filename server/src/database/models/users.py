from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from ...enums.users import Role
from ..connection import Base


class User(Base):
    __tablename__ = "users"

    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str | None]
    login: Mapped[str]
    hashed_password: Mapped[str]
    role: Mapped[Role]
    is_admin: Mapped[bool] = mapped_column(
        server_default=expression.false(),
    )
