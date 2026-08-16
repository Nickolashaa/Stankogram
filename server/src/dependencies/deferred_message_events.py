from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.deferred_message_events import DeferredMessageEventService
from .database import get_session


def get_deferred_message_event_service(
    session: AsyncSession = Depends(get_session),
) -> DeferredMessageEventService:
    return DeferredMessageEventService(session)
