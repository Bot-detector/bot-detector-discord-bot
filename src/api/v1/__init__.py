from fastapi import APIRouter

from src.api.v1 import monitoring, events, verification

router = APIRouter()
router.include_router(monitoring.router, prefix="/monitoring")
router.include_router(verification.router)
router.include_router(events.router)
