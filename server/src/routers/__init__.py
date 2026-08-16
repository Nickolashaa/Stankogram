from fastapi import APIRouter

from .auth import router as auth_router
from .chats import router as chats_router
from .websockets import router as ws_router

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(chats_router)
router.include_router(ws_router)


@router.get("/health", response_model=dict[str, str])
async def health() -> dict[str, str]:
    return {
        "code": "200",
        "message": "Welcome to Stankogram API",
    }
