from ...services.base import Schema
from .attachments import ATTACHMENTS_BY_MESSAGE_ID_LOADER
from .auth import USER_LOADER
from .chats import CHAT_LOADER, CHAT_PARTICIPANTS_BY_CHAT_ID_LOADER
from .messages import LAST_MESSAGE_BY_CHAT_ID_LOADER, MESSAGE_LOADER
from .presence import PRESENCE_LOADER


class DataLoaders(Schema):
    attachments_by_message_id_loader: ATTACHMENTS_BY_MESSAGE_ID_LOADER
    user_loader: USER_LOADER
    chat_loader: CHAT_LOADER
    chat_participants_by_chat_id_loader: CHAT_PARTICIPANTS_BY_CHAT_ID_LOADER
    last_message_by_chat_id_loader: LAST_MESSAGE_BY_CHAT_ID_LOADER
    message_loader: MESSAGE_LOADER
    presence_loader: PRESENCE_LOADER
