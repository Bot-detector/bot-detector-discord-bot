from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.discord_verification import DiscordVerification


class DiscordVerificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, discord_id: int, player_id: int, code: str):
        verification = DiscordVerification(
            discord_id=discord_id, player_id=player_id, code=code
        )
        self.session.add(verification)
        await self.session.commit()
        return verification

    async def read(self, verification_id: int):
        return await self.session.get(DiscordVerification, verification_id)

    async def update(self, verification_id: int, verified_status: bool):
        verification = await self.session.get(DiscordVerification, verification_id)
        if verification:
            verification.verified_status = verified_status
            await self.session.commit()
        return verification

    async def delete(self, verification_id: int):
        verification = await self.session.get(DiscordVerification, verification_id)
        if verification:
            await self.session.delete(verification)
            await self.session.commit()
