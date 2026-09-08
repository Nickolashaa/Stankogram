import asyncio
from pathlib import Path

import asyncpg

from ..config import DATABASE_URL

_TEST_DATA_PATH = Path(__file__).parent / "test_data.sql"


async def _seed() -> None:
    connection = await asyncpg.connect(
        DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    )

    try:
        async with connection.transaction():
            await connection.execute(_TEST_DATA_PATH.read_text(encoding="utf-8"))
    finally:
        await connection.close()

    print("Success!")


def main() -> None:
    asyncio.run(_seed())
