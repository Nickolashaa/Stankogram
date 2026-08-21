from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from ..database.connection import session_maker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
