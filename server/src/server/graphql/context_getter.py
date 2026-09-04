from typing import Annotated

from fastapi import Cookie, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies.auth import get_auth_service, get_current_user
from ..dependencies.chats import get_chat_participant_service, get_chat_service
from ..dependencies.messages import get_message_reaction_service, get_message_service
from ..dependencies.session import get_session
from ..dependencies.system_notifications import get_system_notification_service
from ..services import Services
from ..services.auth import AuthService
from ..services.auth.schemas import UserResponse
from ..services.chats import ChatService
from ..services.chats.participants import ChatParticipantService
from ..services.messages import MessageService
from ..services.messages.reactions import MessageReactionService
from ..services.system_notifications import SystemNotificationService
from .context import AuthorizedContext, Context
from .data_loaders import DataLoaders
from .data_loaders.auth import build_users_loader
from .data_loaders.chats import build_chats_loader
from .data_loaders.messages import (
    build_last_message_by_chat_id_loader,
    build_reactions_by_message_id_loader,
)


async def context_getter(
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
    message_reaction_service: MessageReactionService = Depends(
        get_message_reaction_service
    ),
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
            message_reaction_service=message_reaction_service,
            system_notification_service=system_notification_service,
        ),
        data_loaders=DataLoaders(
            user_loader=build_users_loader(auth_service),
            chat_loader=build_chats_loader(chat_service),
            last_message_by_chat_id_loader=build_last_message_by_chat_id_loader(
                message_service
            ),
            reactions_by_message_id_loader=build_reactions_by_message_id_loader(
                message_reaction_service
            ),
        ),
        refresh_token=refresh_token,
    )
    if current_user is None:
        return context
    return AuthorizedContext.from_context(context=context, current_user=current_user)
