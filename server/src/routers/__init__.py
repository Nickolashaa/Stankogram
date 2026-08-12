from fastapi import APIRouter

from .auth import router as auth_router
from .chats import router as chats_router
from .messages import router as messages_router

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(chats_router)
router.include_router(messages_router)


@router.get("/health", response_model=dict[str, str])
async def health() -> dict[str, str]:
    return {
        "code": "200",
        "message": "Welcome to Stankogram API",
    }
