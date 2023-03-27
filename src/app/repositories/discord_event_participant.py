from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.discord_event_participant import DiscordEventParticipant


class DiscordEventParticipantRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event_id: int, verification_id: int):
        participant = DiscordEventParticipant(
            event_id=event_id, verification_id=verification_id
        )
        self.session.add(participant)
        await self.session.commit()
        return participant

    async def read(self, participant_id: int):
        return await self.session.get(DiscordEventParticipant, participant_id)

    async def update(self, participant_id: int, participating: bool):
        participant = await self.session.get(DiscordEventParticipant, participant_id)
        if participant:
            participant.participating = participating
            await self.session.commit()
        return participant

    async def delete(self, participant_id: int):
        participant = await self.session.get(DiscordEventParticipant, participant_id)
        if participant:
            await self.session.delete(participant)
            await self.session.commit()
