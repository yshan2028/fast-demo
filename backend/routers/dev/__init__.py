from fastapi import APIRouter

from .auth import router as auth_router
from .logging import router as logging_router
from .orm import router as orm_router
from .other import router as other_router
from .params import router as params_router
from .ping import router as ping_router
from .redis import router as redis_router
from .system import router as system_router

router = APIRouter(prefix='/test')

router.include_router(ping_router)
router.include_router(system_router)
router.include_router(logging_router)
router.include_router(orm_router)
router.include_router(redis_router)
router.include_router(auth_router)
router.include_router(params_router)
router.include_router(other_router)
