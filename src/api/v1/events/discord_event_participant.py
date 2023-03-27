from fastapi import APIRouter, Depends, Query, Body
from src.app.repositories.discord_event_participant import (
    DiscordEventParticipantRepository,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.session import get_session
from src.core.fastapi.dependencies.auth import authenticate_user
from typing import Annotated

router = APIRouter()


async def get_discord_event_participant_repository(
    session: AsyncSession = Depends(get_session),
):
    return DiscordEventParticipantRepository(session)


@router.get("/participants")
async def get_discord_event_participants(
    event_id: Annotated[int, Query()] = None,
    participant_id: Annotated[int, Query()] = None,
    usr: bool = Depends(authenticate_user),
    repo: DiscordEventParticipantRepository = Depends(
        get_discord_event_participant_repository
    ),
):
    participants = await repo.read(participant_id, event_id)
    return participants


@router.post("/participants")
async def add_discord_event_participant(
    event_id: Annotated[int, Query(...)],
    verification_id: Annotated[int, Query(...)],
    usr: bool = Depends(authenticate_user),
    repo: DiscordEventParticipantRepository = Depends(
        get_discord_event_participant_repository
    ),
):
    participant = await repo.create(event_id, verification_id)
    return {"id": participant.id}


@router.put("/participants")
async def update_discord_event_participant(
    participant_id: Annotated[int, Query(...)],
    participating: Annotated[bool, Query(...)],
    usr: bool = Depends(authenticate_user),
    repo: DiscordEventParticipantRepository = Depends(
        get_discord_event_participant_repository
    ),
):
    participant = await repo.update(participant_id, participating)
    return {"success": bool(participant)}


@router.delete("/participants")
async def remove_discord_event_participant(
    event_id: Annotated[int, Query(...)],
    participant_id: Annotated[int, Query(...)],
    usr: bool = Depends(authenticate_user),
    repo: DiscordEventParticipantRepository = Depends(
        get_discord_event_participant_repository
    ),
):
    await repo.delete(participant_id, event_id)
    return {"success": True}
