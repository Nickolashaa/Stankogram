from ...services.base import Schema
from .auth import USER_LOADER
from .chats import CHAT_LOADER, CHAT_PARTICIPANTS_BY_CHAT_ID_LOADER
from .messages import LAST_MESSAGE_BY_CHAT_ID_LOADER, MESSAGE_LOADER


class DataLoaders(Schema):
    user_loader: USER_LOADER
    chat_loader: CHAT_LOADER
    chat_participants_by_chat_id_loader: CHAT_PARTICIPANTS_BY_CHAT_ID_LOADER
    last_message_by_chat_id_loader: LAST_MESSAGE_BY_CHAT_ID_LOADER
    message_loader: MESSAGE_LOADER
