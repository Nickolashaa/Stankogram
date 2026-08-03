from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.cancelled_refresh_tokens import CancelledRefreshTokenService
from .database import get_session


def get_cancelled_refresh_token_service(
    session: AsyncSession = Depends(get_session),
) -> CancelledRefreshTokenService:
    return CancelledRefreshTokenService(session)
