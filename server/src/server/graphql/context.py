from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import Info
from strawberry.fastapi import BaseContext

from ..dependencies.auth import get_auth_service
from ..dependencies.session import get_session
from ..services import Services
from ..services.auth import AuthService


@dataclass(slots=True)
class Context(BaseContext):
    session: AsyncSession
    services: Services
    # data_loaders: DataLoaders


async def context_getter(
    session: AsyncSession = Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service),
) -> Context:
    return Context(
        session=session,
        services=Services(
            auth_service=auth_service,
        ),
    )


AppInfo = Info[Context]
