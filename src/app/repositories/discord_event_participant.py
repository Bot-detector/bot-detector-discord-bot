from src.app.models import discord_event_participant
from sqlalchemy import select


class DiscordEventParticipantRepository:
    # CRUD actions of this table
    def __init__(self) -> None:
        self.table = discord_event_participant

    async def get_discord_event_participant(self):
        query = select(self.table)
