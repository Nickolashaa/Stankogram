from collections import defaultdict

from strawberry.dataloader import DataLoader

from ...services.messages import MessageService
from ..types.messages import Message

type MESSAGES_BY_CHAT_ID_LOADER = DataLoader[int, list[Message]]


def build_messages_by_chat_id_loader(
    message_service: MessageService,
) -> MESSAGES_BY_CHAT_ID_LOADER:
    async def load_chats(keys: list[int]) -> list[list[Message]]:
        chat_id_to_messages = defaultdict(list)

        instances = await message_service.get_list(chat_ids=keys)

        for instance in instances:
            chat_id_to_messages[instance.chat_id].append(Message.from_schema(instance))

        return [chat_id_to_messages[key] for key in keys]

    return DataLoader(load_fn=load_chats)
