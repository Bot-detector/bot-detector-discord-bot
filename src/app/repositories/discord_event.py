from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.discord_event import DiscordEvent


class DiscordEventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event_name: str):
        sql = insert(DiscordEvent).values(event_name=event_name)
        result = await self.session.execute(sql)
        await self.session.commit()
        return result.inserted_primary_key[0]

    async def read(self, event_id: int):
        sql = select(DiscordEvent).where(DiscordEvent.id == event_id)
        result = await self.session.execute(sql)
        return result.scalar_one_or_none()

    async def update(self, event_id: int, event_name: str):
        sql = (
            update(DiscordEvent)
            .where(DiscordEvent.id == event_id)
            .values(event_name=event_name)
        )
        result = await self.session.execute(sql)
        await self.session.commit()
        return result.rowcount

    async def delete(self, event_id: int):
        sql = delete(DiscordEvent).where(DiscordEvent.id == event_id)
        result = await self.session.execute(sql)
        await self.session.commit()
        return result.rowcount
