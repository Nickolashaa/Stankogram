from dataclasses import dataclass
from typing import Annotated, Self

from fastapi import Cookie, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import Info
from strawberry.fastapi import BaseContext

from ..dependencies.auth import get_auth_service, get_current_user
from ..dependencies.chats import get_chat_participant_service, get_chat_service
from ..dependencies.session import get_session
from ..services import Services
from ..services.auth import AuthService
from ..services.auth.schemas import UserResponse
from ..services.chats import ChatService
from ..services.chats.participants import ChatParticipantService
from .data_loaders import DataLoaders
from .data_loaders.auth import build_users_loader
from .data_loaders.chats import build_chats_loader


@dataclass(slots=True)
class Context(BaseContext):
    response: Response
    session: AsyncSession
    services: Services
    data_loaders: DataLoaders


@dataclass(slots=True)
class AuthorizedContext(Context):
    refresh_token: str
    current_user: UserResponse

    @classmethod
    def from_context(
        cls, context: Context, refresh_token: str, current_user: UserResponse
    ) -> Self:
        return cls(
            response=context.response,
            session=context.session,
            services=context.services,
            data_loaders=context.data_loaders,
            refresh_token=refresh_token,
            current_user=current_user,
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
) -> Context | AuthorizedContext:
    context = Context(
        response=response,
        session=session,
        services=Services(
            auth_service=auth_service,
            chat_service=chat_service,
            chat_participant_service=chat_participant_service,
        ),
        data_loaders=DataLoaders(
            user_loader=build_users_loader(auth_service),
            chat_loader=build_chats_loader(chat_service),
        ),
    )
    if current_user is None:
        return context
    return AuthorizedContext.from_context(
        context=context, refresh_token=refresh_token, current_user=current_user
    )


AppInfo = Info[Context]
AuthorizedAppInfo = Info[AuthorizedContext]
