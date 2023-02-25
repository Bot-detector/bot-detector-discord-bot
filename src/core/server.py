from fastapi import FastAPI
from src.core.config import CONFIG

# TODO: logging


def create_app() -> FastAPI:
    _app = FastAPI(
        title="FastAPI Boilerplate",
        description="FastAPI Boilerplate by @iam-abbas",
        version=CONFIG.RELEASE_VERSION,
    )
    return _app


app = create_app()
