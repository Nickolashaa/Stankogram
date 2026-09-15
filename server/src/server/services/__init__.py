from .auth import AuthService
from .base import Schema
from .chats import ChatService
from .chats.participants import ChatParticipantService
from .messages import MessageService
from .notifications import NotificationService
from .system_notifications import SystemNotificationService


class Services(Schema):
    auth_service: AuthService
    chat_service: ChatService
    chat_participant_service: ChatParticipantService
    message_service: MessageService
    notification_service: NotificationService
    system_notification_service: SystemNotificationService
