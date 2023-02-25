from fastapi import APIRouter

from .health import router

monitoring_router = APIRouter()
monitoring_router.include_router(router, prefix="v1/health", tags=["Health"])

__all__ = ["monitoring_router"]
