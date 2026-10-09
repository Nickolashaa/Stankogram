from cryptography.fernet import Fernet
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..services.messages import MessageService
from .session import get_session


def get_fernet() -> Fernet:
    return Fernet(settings.ENCRYPTION_KEY)


def get_message_service(
    session: AsyncSession = Depends(get_session),
    fernet: Fernet = Depends(get_fernet),
) -> MessageService:
    return MessageService(session=session, fernet=fernet)
