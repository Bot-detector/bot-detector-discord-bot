from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from src import api
from src.core.config import CONFIG
from src.core.fastapi.middelware import SQLAlchemyMiddleware

# TODO: logging


def init_routers(_app: FastAPI) -> None:
    _app.include_router(api.router)


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(SQLAlchemyMiddleware),
    ]
    return middleware


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Bot-Detector-Discord-API",
        description="Bot-Detector-Discord-API",
        version=CONFIG.RELEASE_VERSION,
        middleware=make_middleware(),
    )
    init_routers(_app=_app)
    return _app


app = create_app()
