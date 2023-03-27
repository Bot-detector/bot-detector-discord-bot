from sqlalchemy import insert, select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.discord_verification import DiscordVerification


class DiscordVerificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, discord_id: int, player_id: int, code: str):
        sql = insert(DiscordVerification).values(
            discord_id=discord_id, player_id=player_id, code=code
        )
        result = await self.session.execute(sql)
        await self.session.commit()
        return result.inserted_primary_key[0]

    async def read(self, verification_id: int, player_id: int):
        sql = select(DiscordVerification).where(
            or_(
                DiscordVerification.id == verification_id,
                DiscordVerification.player_id == player_id,
            )
        )
        result = await self.session.execute(sql)
        return result.scalar_one_or_none()

    async def update(self, verification_id: int, verified_status: bool):
        sql = (
            update(DiscordVerification)
            .where(DiscordVerification.id == verification_id)
            .values(verified_status=verified_status)
        )
        await self.session.execute(sql)
        await self.session.commit()

    async def delete(self, verification_id: int):
        sql = delete(DiscordVerification).where(
            DiscordVerification.id == verification_id
        )
        await self.session.execute(sql)
        await self.session.commit()
