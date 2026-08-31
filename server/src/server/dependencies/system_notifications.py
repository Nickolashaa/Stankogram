from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.system_notifications import SystemNotificationService
from .session import get_session


async def get_system_notification_service(
    session: AsyncSession = Depends(get_session),
) -> SystemNotificationService:
    return SystemNotificationService(session)
