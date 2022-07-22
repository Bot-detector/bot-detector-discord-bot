import logging
import time

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Header, Query
from pydantic import BaseModel
from sqlalchemy.sql.expression import insert, select, update
from src.database.database import DISCORD_ENGINE
from src.database.models import discordVerification
from sqlalchemy.sql import Select
from src.config import api


logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("v1/verification")
async def get_verification(
    token: str = Header(None),
    name: str = Query(min_length=0, max_length=13)
    ):
    """
    This route queries the discord database for verification
    """
    #TODO: validate token with the api
    
    # get player dict from api
    player = await api.get_player(name=name)

    # check if player exists
    if not player:
        raise HTTPException(status_code=400, detail='player does not exist')

    # create query
    sql:Select = select(discordVerification)
    sql = sql.where(discordVerification.player_id == player['id'])

    async with DISCORD_ENGINE.get_session() as session:
        session: AsyncSession = session
        async with session.begin():
            data = await session.execute(sql)

    return data


@router.post("v1/verification")
async def post_verification(
    token: str = Header(None),
    player_id: int = Query(None),
    discord_id: int = Query(None),
    code: int = Query(None)
    ):
    """
    this route creates a verification record
    """
    return

@router.put("v1/verification")
async def post_verification(
    token: str = Header(None, description="moderator token"),
    name: int = Query(None),
    code: int = Query(None)
    ):
    """
    this route updates a verification record
    """
    return