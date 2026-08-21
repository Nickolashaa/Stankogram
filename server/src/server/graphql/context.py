from dataclasses import dataclass

from fastapi import Depends
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
    session: AsyncSession
    services: Services
    # data_loaders: DataLoaders
    current_user: UserResponse | None


async def context_getter(
    session: AsyncSession = Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service),
    current_user: UserResponse | None = Depends(get_current_user),
) -> Context:
    return Context(
        session=session,
        services=Services(
            auth_service=auth_service,
        ),
        current_user=current_user,
    )


AppInfo = Info[Context]
