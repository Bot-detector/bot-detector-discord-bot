import asyncio
import logging
from typing import Optional

from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from src import bot, config
from src.config import SQL_URI
from src.services.discordApi import discordAPI
from src.database.models import discordVerificationCreate, discordVerificationRead

logger = logging.getLogger(__name__)
app = FastAPI()


@app.get("/")
async def read_root():
    return {"detail": "hello world"}


ENGINE = create_async_engine(SQL_URI, echo=True)
API = discordAPI(ENGINE)


async def init_db():
    async with ENGINE.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    # asyncio.create_task(bot.bot.start(config.TOKEN))
    await init_db()


class PaginationParams(BaseModel):
    limit: int = Query(default=10, gt=0, lt=100)
    offset: int = Query(default=0, ge=0)


@app.get(
    "/discord_verifications",
    response_model=list[discordVerificationRead],
    response_model_exclude_unset=True,
)
async def get_discord_verifications(
    pagination_params: PaginationParams,
    entry: Optional[int] = None,
    player_id: Optional[int] = None,
    discord_id: Optional[str] = None,
):
    return await API.get_discord_verifications(
        pagination_params=pagination_params,
        entry=entry,
        player_id=player_id,
        discord_id=discord_id,
    )


@app.post("/discord_verifications", response_model=discordVerificationRead)
async def create_discord_verification(user: discordVerificationCreate):
    return await API.create_discord_verification(user=user)
