from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import Info
from strawberry.fastapi import BaseContext

from ..services import Services
from ..services.auth.schemas import UserResponse

if TYPE_CHECKING:
    from .data_loaders import DataLoaders


@dataclass(slots=True)
class Context(BaseContext):
    response: Response
    session: AsyncSession
    services: Services
    data_loaders: DataLoaders
    refresh_token: str | None


@dataclass(slots=True)
class AuthorizedContext(Context):
    current_user: UserResponse

    @classmethod
    def from_context(cls, context: Context, current_user: UserResponse) -> Self:
        return cls(
            response=context.response,
            session=context.session,
            services=context.services,
            data_loaders=context.data_loaders,
            refresh_token=context.refresh_token,
            current_user=current_user,
        )


AppInfo = Info[Context]
AuthorizedAppInfo = Info[AuthorizedContext]
