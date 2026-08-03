from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from ..connection import Base


class CancelledToken(Base):
    __tablename__ = "cancelled_tokens"

    jti: Mapped[UUID] = mapped_column(unique=True)
