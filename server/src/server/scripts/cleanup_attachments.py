import asyncio
from datetime import UTC, datetime, timedelta

from ..database.connection import session_maker
from ..services.attachments import AttachmentService
from ..services.storage import StorageService

ORPHAN_AGE_HOURS = 24


async def _cleanup() -> None:
    threshold = datetime.now(UTC) - timedelta(hours=ORPHAN_AGE_HOURS)

    async with session_maker() as session:
        service = AttachmentService(session)

        orphans = [
            instance
            for instance in await service.get_list(is_attached=False)
            if instance.created_at < threshold
        ]
        if not orphans:
            print("No orphaned attachments found.")
            return

        await StorageService().delete(AttachmentService.object_keys(orphans))
        await service.delete([instance.id for instance in orphans])
        await session.commit()

    print(f"Success. Removed {len(orphans)} orphaned attachments.")


def main() -> None:
    asyncio.run(_cleanup())
