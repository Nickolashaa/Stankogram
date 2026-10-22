from cryptography.fernet import Fernet
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.messages import MessageService
from .encryption import get_fernet
from .session import get_session


def get_message_service(
    session: AsyncSession = Depends(get_session),
    fernet: Fernet = Depends(get_fernet),
) -> MessageService:
    return MessageService(session=session, fernet=fernet)
