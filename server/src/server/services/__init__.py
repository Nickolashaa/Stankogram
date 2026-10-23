from .attachments import AttachmentService
from .auth import AuthService
from .base import Schema
from .chats import ChatService
from .chats.participants import ChatParticipantService
from .events import EventService
from .messages import MessageService
from .notifications import NotificationService
from .password_reset import PasswordResetService
from .presence import PresenceService
from .rate_limit import RateLimitService
from .storage import StorageService
from .system_notifications import SystemNotificationService


class Services(Schema):
    attachment_service: AttachmentService
    auth_service: AuthService
    chat_service: ChatService
    chat_participant_service: ChatParticipantService
    message_service: MessageService
    notification_service: NotificationService
    event_service: EventService
    password_reset_service: PasswordResetService
    presence_service: PresenceService
    rate_limit_service: RateLimitService
    storage_service: StorageService
    system_notification_service: SystemNotificationService
