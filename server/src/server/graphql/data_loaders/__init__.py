from ...services.base import Schema
from .auth import USER_LOADER
from .chats import CHAT_LOADER


class DataLoaders(Schema):
    user_loader: USER_LOADER
    chat_loader: CHAT_LOADER
