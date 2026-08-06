import uvicorn

from .config import UVICORN_HOST, UVICORN_PORT

if __name__ == "__main__":
    uvicorn.run("src.server:app", host=UVICORN_HOST, port=UVICORN_PORT)
