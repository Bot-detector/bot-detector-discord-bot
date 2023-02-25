from fastapi import FastAPI
from src.core.config import CONFIG

# TODO: logging


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Bot-Detector-Discord-API",
        description="Bot-Detector-Discord-API",
        version=CONFIG.RELEASE_VERSION,
    )
    return _app


app = create_app()
