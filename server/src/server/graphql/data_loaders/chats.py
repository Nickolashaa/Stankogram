from strawberry.dataloader import DataLoader

from ...services.chats import ChatService
from ...services.chats.participants import ChatParticipantService
from ...services.chats.participants.schemas import ChatParticipantResponse
from ..types.chats import Chat

type CHAT_LOADER = DataLoader[int, Chat]
type CHAT_PARTICIPANTS_BY_CHAT_ID_LOADER = DataLoader[
    int, list[ChatParticipantResponse]
]


def build_chats_loader(chat_service: ChatService) -> CHAT_LOADER:
    async def load_fn(keys: list[int]) -> list[Chat]:
        chat_id_to_chats = {
            chat.id: chat for chat in await chat_service.get_list(ids=keys)
        }

        return [
            Chat.from_schema(instance)
            for instance in [chat_id_to_chats[key] for key in keys]
        ]

    return DataLoader(load_fn=load_fn)


def build_chat_participants_by_chat_id_loader(
    chat_participant_service: ChatParticipantService,
) -> CHAT_PARTICIPANTS_BY_CHAT_ID_LOADER:
    async def load_fn(keys: list[int]) -> list[list[ChatParticipantResponse]]:
        chat_id_to_links: dict[int, list[ChatParticipantResponse]] = {}

        instances = await chat_participant_service.get_list(chat_ids=keys)

        for instance in instances:
            chat_id_to_links.setdefault(instance.chat_id, []).append(instance)

        return [chat_id_to_links.get(key, []) for key in keys]

    return DataLoader(load_fn=load_fn)
