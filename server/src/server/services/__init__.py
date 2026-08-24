from .auth import AuthService
from .base import Schema
from .chats import ChatService
from .chats.participants import ChatParticipantService
from .messages import MessageService


class Services(Schema):
    auth_service: AuthService
    chat_service: ChatService
    chat_participant_service: ChatParticipantService
    message_service: MessageService
