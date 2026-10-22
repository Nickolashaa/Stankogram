from .auth import AuthService
from .base import Schema
from .chats import ChatService
from .chats.participants import ChatParticipantService
from .events import EventService
from .messages import MessageService
from .notifications import NotificationService
from .presence import PresenceService
from .system_notifications import SystemNotificationService


class Services(Schema):
    auth_service: AuthService
    chat_service: ChatService
    chat_participant_service: ChatParticipantService
    message_service: MessageService
    notification_service: NotificationService
    event_service: EventService
    presence_service: PresenceService
    system_notification_service: SystemNotificationService
