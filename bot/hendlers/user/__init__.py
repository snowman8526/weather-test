__all__ = ('router',)

from aiogram import Router

from .user_hendlers import router as user_hendlers_router

router = Router()
router.include_router(user_hendlers_router)
