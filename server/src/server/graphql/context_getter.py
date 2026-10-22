from typing import Annotated

from fastapi import Cookie, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import HTTPConnection

from ..dependencies.auth import get_auth_service, get_current_user
from ..dependencies.chats import get_chat_participant_service, get_chat_service
from ..dependencies.events import get_event_service
from ..dependencies.messages import get_message_service
from ..dependencies.notifications import get_notification_service
from ..dependencies.presence import get_presence_service
from ..dependencies.session import get_session
from ..dependencies.system_notifications import get_system_notification_service
from ..services import Services
from ..services.auth import AuthService
from ..services.auth.schemas import UserResponse
from ..services.chats import ChatService
from ..services.chats.participants import ChatParticipantService
from ..services.events import EventService
from ..services.messages import MessageService
from ..services.notifications import NotificationService
from ..services.presence import PresenceService
from ..services.system_notifications import SystemNotificationService
from .context import AuthorizedContext, Context
from .data_loaders import DataLoaders
from .data_loaders.auth import build_users_loader
from .data_loaders.chats import (
    build_chat_participants_by_chat_id_loader,
    build_chats_loader,
)
from .data_loaders.messages import (
    build_last_message_by_chat_id_loader,
    build_messages_loader,
)
from .data_loaders.presence import build_presence_loader


def _get_client_ip(connection: HTTPConnection) -> str:
    forwarded_for = connection.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.rsplit(",", 1)[-1].strip()

    return connection.client.host if connection.client else ""


async def context_getter(
    connection: HTTPConnection,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    session: AsyncSession = Depends(get_session),
    current_user: UserResponse | None = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
    chat_service: ChatService = Depends(get_chat_service),
    chat_participant_service: ChatParticipantService = Depends(
        get_chat_participant_service
    ),
    message_service: MessageService = Depends(get_message_service),
    notification_service: NotificationService = Depends(get_notification_service),
    event_service: EventService = Depends(get_event_service),
    presence_service: PresenceService = Depends(get_presence_service),
    system_notification_service: SystemNotificationService = Depends(
        get_system_notification_service
    ),
) -> Context | AuthorizedContext:
    context = Context(
        response=response,
        session=session,
        services=Services(
            auth_service=auth_service,
            chat_service=chat_service,
            chat_participant_service=chat_participant_service,
            message_service=message_service,
            notification_service=notification_service,
            event_service=event_service,
            presence_service=presence_service,
            system_notification_service=system_notification_service,
        ),
        data_loaders=DataLoaders(
            user_loader=build_users_loader(auth_service),
            chat_loader=build_chats_loader(chat_service),
            chat_participants_by_chat_id_loader=(
                build_chat_participants_by_chat_id_loader(chat_participant_service)
            ),
            last_message_by_chat_id_loader=build_last_message_by_chat_id_loader(
                message_service
            ),
            message_loader=build_messages_loader(message_service),
            presence_loader=build_presence_loader(presence_service),
        ),
        refresh_token=refresh_token,
        client_ip=_get_client_ip(connection),
    )
    if current_user is None:
        return context
    return AuthorizedContext.from_context(context=context, current_user=current_user)
