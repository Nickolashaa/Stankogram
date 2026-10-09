import uvicorn

from .app import app
from .config import settings


def main() -> None:
    uvicorn.run(app, host=settings.UVICORN_HOST, port=settings.UVICORN_PORT)
