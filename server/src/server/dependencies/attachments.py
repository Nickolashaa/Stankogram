from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.attachments import AttachmentService
from .session import get_session


async def get_attachment_service(
    session: AsyncSession = Depends(get_session),
) -> AttachmentService:
    return AttachmentService(session)
