from dataclasses import dataclass
from typing import Annotated

from fastapi import Cookie, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import Info
from strawberry.fastapi import BaseContext

from ..dependencies.auth import get_auth_service, get_current_user
from ..dependencies.session import get_session
from ..services import Services
from ..services.auth import AuthService
from ..services.auth.schemas import UserResponse


@dataclass(slots=True)
class Context(BaseContext):
    response: Response
    refresh_token: str | None
    session: AsyncSession
    current_user: UserResponse | None
    services: Services
    # data_loaders: DataLoaders


async def context_getter(
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    session: AsyncSession = Depends(get_session),
    current_user: UserResponse | None = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> Context:
    return Context(
        response=response,
        refresh_token=refresh_token,
        session=session,
        current_user=current_user,
        services=Services(
            auth_service=auth_service,
        ),
    )


AppInfo = Info[Context]
