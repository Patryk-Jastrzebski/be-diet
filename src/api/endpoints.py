from fastapi import APIRouter

from src.api.auth.auth import auth_router
from src.api.user.user import user_router

router = APIRouter()
router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])


__all__ = ["router"]