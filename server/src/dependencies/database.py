from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from ..database.connection import session_maker


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_maker() as session:
        yield session
