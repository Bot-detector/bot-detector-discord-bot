from sqlalchemy import and_, insert, select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.discord_event_participant import DiscordEventParticipant


class DiscordEventParticipantRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event_id: int, verification_id: int):
        sql = insert(DiscordEventParticipant).values(
            event_id=event_id, verification_id=verification_id
        )
        result = await self.session.execute(sql)
        await self.session.commit()
        return result.inserted_primary_key[0]

    async def read(self, participant_id: int = None, event_id: int = None):
        sql = select(DiscordEventParticipant)
        if participant_id is not None:
            sql = sql.where(DiscordEventParticipant.verification_id == participant_id)
        if event_id is not None:
            sql = sql.where(DiscordEventParticipant.event_id == event_id)

        result = await self.session.execute(sql)
        return result.scalars().all()

    async def update(self, participant_id: int, participating: bool):
        sql = (
            update(DiscordEventParticipant)
            .where(DiscordEventParticipant.verification_id == participant_id)
            .values(participating=participating)
        )
        await self.session.execute(sql)
        await self.session.commit()

    async def delete(self, participant_id: int, event_id: int):
        sql = delete(DiscordEventParticipant).where(
            and_(
                DiscordEventParticipant.verification_id == participant_id,
                DiscordEventParticipant.event_id == event_id,
            )
        )
        await self.session.execute(sql)
        await self.session.commit()
