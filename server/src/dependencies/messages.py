from cryptography.fernet import Fernet
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import ENCRYPTION_KEY
from ..services import ChatService, MessageService
from .chats import get_chat_service
from .database import get_session


def get_message_service(
    session: AsyncSession = Depends(get_session),
    chat_service: ChatService = Depends(get_chat_service),
) -> MessageService:
    return MessageService(
        session=session,
        fernet=Fernet(ENCRYPTION_KEY),
        chat_service=chat_service,
    )
