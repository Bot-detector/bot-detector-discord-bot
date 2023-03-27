from fastapi import APIRouter, Depends, Query, Body
from src.app.repositories.discord_event import (
    DiscordEventRepository,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.session import get_session
from src.core.fastapi.dependencies.auth import authenticate_user
from typing import Annotated


async def get_discord_event_repository(
    session: AsyncSession = Depends(get_session),
):
    return DiscordEventRepository(session)


router = APIRouter()


@router.get("/")
async def get_discord_event(
    event_id: Annotated[int, Query()] = None,
    event_name: Annotated[str, Query()] = None,
    usr: bool = Depends(authenticate_user),
    repo: DiscordEventRepository = Depends(get_discord_event_repository),
):
    event = await repo.read(event_id, event_name)
    return event


@router.post("/")
async def create_discord_event(
    event_name: Annotated[str, Body(...)],
    usr: bool = Depends(authenticate_user),
    repo: DiscordEventRepository = Depends(get_discord_event_repository),
):
    event_id = await repo.create(event_name)
    return {"event_id": event_id}


@router.put("/")
async def update_discord_event(
    event_id: Annotated[int, Body(...)],
    event_name: Annotated[str, Body(...)],
    usr: bool = Depends(authenticate_user),
    repo: DiscordEventRepository = Depends(get_discord_event_repository),
):
    updated_rows = await repo.update(event_id, event_name)
    return {"updated_rows": updated_rows}


@router.delete("/")
async def delete_discord_event(
    event_id: Annotated[int, Query(...)],
    usr: bool = Depends(authenticate_user),
    repo: DiscordEventRepository = Depends(get_discord_event_repository),
):
    deleted_rows = await repo.delete(event_id)
    return {"deleted_rows": deleted_rows}
