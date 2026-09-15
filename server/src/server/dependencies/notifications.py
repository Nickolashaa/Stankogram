from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.notifications import NotificationService
from .session import get_session


def get_notification_service(
    session: AsyncSession = Depends(get_session),
) -> NotificationService:
    return NotificationService(session)
