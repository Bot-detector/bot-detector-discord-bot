from fastapi import APIRouter

from src.api.v1 import monitoring, events, verification

router = APIRouter()
router.include_router(monitoring.router, prefix="/monitoring")
# v1_router.include_router(events.router, prefix="/events")
# v1_router.include_router(verification.router, prefix="/verification")
