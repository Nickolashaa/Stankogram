from ...enums.chats import ChatType
from ...schemas.chats import ChatResponse
from ..exceptions import ObjectNotFound
from .service import ChatService
from .to_users_service import ChatToUserService


class ChatManager:
    def __init__(
        self, chat_service: ChatService, chat_to_user_service: ChatToUserService
    ) -> None:
        self._chat_service = chat_service
        self._chat_to_user_service = chat_to_user_service

    async def get_or_create(
        self,
        first_user_id: int,
        second_user_id: int,
    ) -> ChatResponse:
        try:
            chat_to_user = await self._chat_to_user_service.get_by_participants(
                first_user_id=first_user_id,
                second_user_id=second_user_id,
            )
            return await self._chat_service.get(chat_to_user.chat_id)
        except ObjectNotFound:
            pass

        chat = await self._chat_service.create(type=ChatType.PRIVATE)

        await self._chat_to_user_service.create(user_id=first_user_id, chat_id=chat.id)
        await self._chat_to_user_service.create(user_id=second_user_id, chat_id=chat.id)

        return chat
