from strawberry.dataloader import DataLoader

from ...services.messages import MessageService
from ...services.messages.reactions import MessageReactionService
from ..types.messages import Message, MessageReaction

type LAST_MESSAGE_BY_CHAT_ID_LOADER = DataLoader[int, Message | None]
type REACTIONS_BY_MESSAGE_ID_LOADER = DataLoader[int, list[MessageReaction]]


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


def build_reactions_by_message_id_loader(
    message_reaction_service: MessageReactionService,
) -> REACTIONS_BY_MESSAGE_ID_LOADER:
    async def load_fn(keys: list[int]) -> list[list[MessageReaction]]:
        message_id_to_reactions: dict[int, list[MessageReaction]] = {}

        instances = await message_reaction_service.get_list(message_ids=keys)

        for instance in instances:
            message_id_to_reactions.setdefault(instance.message_id, []).append(
                MessageReaction.from_schema(instance)
            )

        return [message_id_to_reactions.get(key, []) for key in keys]

    return DataLoader(load_fn=load_fn)
