from cryptography.fernet import Fernet
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import ENCRYPTION_KEY
from ..services import MessagesService
from .database import get_session


def get_messages_service(
    session: AsyncSession = Depends(get_session),
) -> MessagesService:
    return MessagesService(
        session=session,
        fernet=Fernet(ENCRYPTION_KEY),
    )
