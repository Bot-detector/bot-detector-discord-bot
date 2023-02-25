from fastapi import FastAPI
from src.core.config import CONFIG
from src import api

# TODO: logging


def init_routers(_app: FastAPI) -> None:
    _app.include_router(api.router)


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Bot-Detector-Discord-API",
        description="Bot-Detector-Discord-API",
        version=CONFIG.RELEASE_VERSION,
    )
    init_routers(_app=_app)
    return _app


app = create_app()
