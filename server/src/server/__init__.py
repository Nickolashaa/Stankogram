import uvicorn

from .app import app
from .config import UVICORN_HOST, UVICORN_PORT


def main() -> None:
    uvicorn.run(app, host=UVICORN_HOST, port=UVICORN_PORT)
