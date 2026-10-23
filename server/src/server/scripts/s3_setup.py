import asyncio
import sys

from botocore.exceptions import ClientError

from ..config import settings
from ..services.storage import StorageService


async def _setup(origins: list[str]) -> None:
    storage = StorageService()

    try:
        await storage.check_access()
    except ClientError as e:
        print(f"Bucket {settings.S3_BUCKET} is not reachable: {e}")
        raise SystemExit(1)

    print(f"Bucket {settings.S3_BUCKET} at {settings.S3_ENDPOINT_URL} is reachable.")

    try:
        allowed = await storage.set_cors(origins)
    except ClientError as e:
        print(f"Could not set CORS, configure it in the provider console: {e}")
        raise SystemExit(1)

    print(f"Success. Browser uploads are allowed from: {', '.join(allowed)}")


def main() -> None:
    origins = sys.argv[1:] or [settings.APP_BASE_URL]
    asyncio.run(_setup(origins))
