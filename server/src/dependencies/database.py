from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from ..database.connection import session_maker


async def get_session() -> AsyncGenerator[AsyncSession]:
    session = session_maker()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
