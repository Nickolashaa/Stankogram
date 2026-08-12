from fastapi import APIRouter

from .private import router as private_chats_router

router = APIRouter(prefix="/chats", tags=["chats"])
router.include_router(private_chats_router)
