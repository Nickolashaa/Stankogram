from fastapi import APIRouter

from ..schemas.base import HealthResponse
from .auth import router as auth_router
from .users import router as users_router

router = APIRouter(prefix="/api")
router.include_router(users_router)
router.include_router(auth_router)


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(code=200, message="Welcome to Stankogram API")
