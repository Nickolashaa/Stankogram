from strawberry.dataloader import DataLoader

from ...services.chats import ChatService
from ..types.chats import Chat

type CHAT_LOADER = DataLoader[int, Chat]


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
