from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import APP_BASE_URL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[APP_BASE_URL],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
