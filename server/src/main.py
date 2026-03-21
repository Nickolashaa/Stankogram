import uvicorn
from config import config


def main() -> None:
    uvicorn.run(
        "src.server:app",
        host=config.uvicorn_host,
        port=config.uvicorn_port,
    )
