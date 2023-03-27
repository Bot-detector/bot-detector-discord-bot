from fastapi import APIRouter

from src.api.v1.events import discord_event, discord_event_participant

router = APIRouter()
router.include_router(discord_event.router, prefix="/discord-events", tags=["Events"])
router.include_router(
    discord_event_participant.router, prefix="/discord-events", tags=["Events"]
)
