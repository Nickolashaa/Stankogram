from cryptography.fernet import Fernet
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import ENCRYPTION_KEY
from ..services import MessageService
from .database import _get_session


def get_message_service(
    session: AsyncSession = Depends(_get_session),
) -> MessageService:
    return MessageService(
        session=session,
        fernet=Fernet(ENCRYPTION_KEY),
    )
