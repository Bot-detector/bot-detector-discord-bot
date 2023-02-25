from fastapi import APIRouter

from src.app.schemas.extras.health import Health
from src.core.config import CONFIG

router = APIRouter()


@router.get("/", response_model=Health)
async def health() -> Health:
    return Health(version=CONFIG.RELEASE_VERSION, status="Healthy")
