from fastapi import APIRouter

from src.api.v1.verification import verification

router = APIRouter()
router.include_router(
    verification.router, prefix="/verifications", tags=["Verification"]
)
