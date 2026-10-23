from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from ...enums.attachments import AttachmentKind
from ..connection import Base
from .auth import User
from .chats import Chat
from .messages import Message


class Attachment(Base):
    __tablename__ = "attachments"

    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    message_id: Mapped[int | None] = mapped_column(
        ForeignKey(Message.id, ondelete="CASCADE"),
    )
    kind: Mapped[AttachmentKind]
    key: Mapped[str] = mapped_column(unique=True)
    thumbnail_key: Mapped[str | None]
    name: Mapped[str]
    content_type: Mapped[str]
    size: Mapped[int]
    width: Mapped[int | None]
    height: Mapped[int | None]
    duration_ms: Mapped[int | None]

    __table_args__ = (Index("ix_attachments_message_id", "message_id"),)
