from fastapi import APIRouter

from src.api.v1.monitoring import health

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["Health"])
