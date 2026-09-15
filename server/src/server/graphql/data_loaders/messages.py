from strawberry.dataloader import DataLoader

from ...services.messages import MessageService
from ..types.messages import Message

type LAST_MESSAGE_BY_CHAT_ID_LOADER = DataLoader[int, Message | None]
type MESSAGE_LOADER = DataLoader[int, Message]


def build_messages_loader(
    message_service: MessageService,
) -> MESSAGE_LOADER:
    async def load_fn(keys: list[int]) -> list[Message]:
        message_id_to_message = {
            instance.id: Message.from_schema(instance)
            for instance in await message_service.get_list(ids=keys)
        }

        return [message_id_to_message[key] for key in keys]

    return DataLoader(load_fn=load_fn)


def build_last_message_by_chat_id_loader(
    message_service: MessageService,
) -> LAST_MESSAGE_BY_CHAT_ID_LOADER:
    async def load_fn(keys: list[int]) -> list[Message | None]:
        chat_id_to_message: dict[int, Message] = {}

        instances = await message_service.get_list(chat_ids=keys)

        for instance in instances:
            chat_id_to_message.setdefault(
                instance.chat_id, Message.from_schema(instance)
            )

        return [chat_id_to_message.get(key) for key in keys]

    return DataLoader(load_fn=load_fn)
