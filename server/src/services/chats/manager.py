from .private import PrivateChatService
from .public import PublicChatService
from .messages import MessageService
from ..base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from ...database.models.chats import ChatParticipant
from typing import Sequence
from ...schemas.chats import ChatProfile
from ..auth import AuthService
from .types import MessageCreateParams
from typing import Unpack
from ...schemas.messages import MessageResponse
from ...exceptions import Forbidden

class ChatManager(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        private_chat_service: PrivateChatService,
        public_chat_service: PublicChatService,
        message_service: MessageService,
        auth_service: AuthService,
    ) -> None:
        super().__init__(session)
        self._private_chat_service = private_chat_service
        self._public_chat_service = public_chat_service
        self._message_service = message_service
        self._auth_service = auth_service

    async def get_recipient_ids(
        self,
        chat_id: int,
    ) -> Sequence[int]:
        stmt = select(ChatParticipant.user_id).where(ChatParticipant.chat_id == chat_id)

        res = await self._session.execute(stmt)

        return res.scalars().all()

    async def can_message_to_chat(
        self,
        user_id: int,
        chat_id: int,
    ) -> bool:
        stmt = select(exists()).where(
            ChatParticipant.user_id == user_id,
            ChatParticipant.chat_id == chat_id,
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def get_or_create_private_chat(
        self,
        user_id: int,
        participant_id: int,
    ) -> ChatProfile:
        chat = await self._private_chat_service.get_private_chat_or_create(
            user_id=user_id,
            participant_id=participant_id,
        )

        last_message = await self._message_service.get_last_message(chat_id=chat.id)

        participant = await self._auth_service.get(id=participant_id)
        
        return ChatProfile(
            chat=chat,
            last_message=last_message,
            title=participant.full_name,
        )

    async def send_message(
        self,
        **data: Unpack[MessageCreateParams],
    ) -> MessageResponse:
        if (
            await self.can_message_to_chat(
                chat_id=data.get("chat_id"),
                user_id=data.get("user_id"),
            )
            is False
        ):
            raise Forbidden("Dont have access to this chat.")
