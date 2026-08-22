from .auth import AuthService
from .base import Schema
from .chats import ChatService


class Services(Schema):
    auth_service: AuthService
    chat_service: ChatService
