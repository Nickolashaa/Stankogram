from fastapi import APIRouter

from .users import router as users_router

router = APIRouter(prefix="/api")
router.include_router(users_router)


@router.get("/health")
async def health() -> dict[str, str]:
    return {
        "code": "200",
        "message": "Welcome to Stankogram API",
    }
