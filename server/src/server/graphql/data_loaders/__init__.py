from pydantic import BaseModel

from .auth import USER_LOADER
from .chats import CHAT_LOADER


class DataLoaders(BaseModel):
    user_loader: USER_LOADER
    chat_loader: CHAT_LOADER
