from typing import Unpack

from cryptography.fernet import Fernet
from sqlalchemy import func, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from ...database.models.auth import User
from ...database.models.chats import Chat, ChatParticipant
from ...database.models.messages import Message

from ...enums.chats import ChatType
from ...exceptions import InvalidInput, ObjectNotFound
from ...schemas.chats import ChatProfile, ChatResponse
from ...schemas.messages import MessageResponse
from ...schemas.users import UserResponse
from ..base import BaseService
from .types import ChatCreateParams


class ChatService(BaseService):
    def __init__(self, session: AsyncSession, fernet: Fernet) -> None:
        super().__init__(session)
        self._fernet = fernet

    async def create(self, **data: Unpack[ChatCreateParams]) -> ChatResponse:
        if data.get("type") == ChatType.PRIVATE and data.get("title") is not None:
            raise InvalidInput("Private chat cannot have title")

        if data.get("type") == ChatType.PUBLIC and data.get("title") is None:
            raise InvalidInput("Public chat must have title")

        stmt = insert(Chat).values(**data).returning(Chat)

        res = await self._session.execute(stmt)

        return ChatResponse.model_validate(res.scalar_one())

    async def get(
        self,
        id: int,
    ) -> ChatResponse:
        stmt = select(Chat).where(Chat.id == id)

        try:
            res = await self._session.execute(stmt)
        except IntegrityError:
            raise ObjectNotFound(f"Chat with id {id} not found")

        return ChatResponse.model_validate(res.scalar_one())

    @staticmethod
    def _build_last_messsage_subq():
        return (
            select(
                Message.chat_id, func.max(Message.updated_at).label("max_updated_at")
            )
            .group_by(Message.chat_id)
            .subquery()
        )

    async def _get_list_private(
        self,
        user_id: int,
        search_query: str | None = None,
    ) -> list[ChatProfile]:
        last_message_subq = self._build_last_messsage_subq()

        stmt = (
            select(Chat, Message, User)
            .join(Message, Message.chat_id == Chat.id)
            .join(
                last_message_subq,
                (Message.chat_id == last_message_subq.c.chat_id)
                & (Message.updated_at == last_message_subq.c.max_updated_at)
            )
            .join(
                ChatParticipant,
                (ChatParticipant.chat_id == Chat.id)
                & (ChatParticipant.user_id != user_id)
            )
            .join(
                User, User.id == ChatParticipant.user_id
            )
            .where(Chat.type == ChatType.PRIVATE)
        )

        if search_query is not None:
            stmt = stmt.where(User.full_name.icontains(search_query))

        res = await self._session.execute(stmt)

        return [
            ChatProfile.model_validate(entity)
            for entity in res.scalars().all()
        ]


    @staticmethod
    def _build_chat_list_for_user_stmt(
        user_id: int,
        search_query: str | None = None,
    ):
        my_participation = aliased(ChatParticipant)
        other_participant = aliased(ChatParticipant)
        other_user = aliased(User)

        last_message_subq = (
            select(Message)
            .where(Message.chat_id == Chat.id)
            .order_by(Message.updated_at.desc())
            .limit(1)
            .correlate(Chat)
            .scalar_subquery()
        )

        base = (
            select(
                Chat,
                last_message_subq.label("last_message"),
            )
            .join(
                my_participation,
                (my_participation.chat_id == Chat.id)
                & (my_participation.user_id == user_id),
            )
            .outerjoin(
                other_participant,
                (other_participant.chat_id == Chat.id)
                & (other_participant.user_id != user_id)
                & (Chat.type == ChatType.PRIVATE),
            )
            .outerjoin(other_user, other_user.id == other_participant.user_id)
        ).subquery("chat_meta")

        stmt = select(base)

        if search_query is not None:
            stmt = stmt.where(base.c.title.icontains(search_query))

        stmt = stmt.order_by(base.c.last_message_at.desc().nulls_last())

        return stmt
