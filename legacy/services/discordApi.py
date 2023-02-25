from pydantic import BaseModel, Field
from sqlmodel import select
from src.database.models import (
    discordVerification,
    discordVerificationCreate,
    discordVerificationRead,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Optional


class PaginationParams(BaseModel):
    limit: int = Field(default=10, gt=0, lt=100)
    offset: int = Field(default=0, ge=0)


class discordAPI:
    def __init__(self, engine):
        """
        Initialize the discordAPI class with a database engine.

        Parameters:
            engine: The database engine to use for the discordAPI.
        """
        self.session_factory = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_discord_verifications(
        self,
        pagination_params: PaginationParams,
        entry: Optional[int] = None,
        player_id: Optional[int] = None,
        discord_id: Optional[str] = None,
    ) -> list[discordVerification]:
        """
        Get a list of discord verifications from the database.

        Parameters:
            pagination_params: The pagination parameters for the query.
            entry: An optional entry ID to filter the results by.
            player_id: An optional player ID to filter the results by.
            discord_id: An optional Discord ID to filter the results by.

        Returns:
            A list of discord verifications that match the specified filters.
        """
        statement = (
            select(discordVerification)
            .offset(pagination_params.offset)
            .limit(pagination_params.limit)
        )
        if entry:
            statement = statement.where(discordVerification.Entry == entry)
        if player_id:
            statement = statement.where(discordVerification.Player_id == player_id)
        if discord_id:
            statement = statement.where(discordVerification.Discord_id == discord_id)

        async with self.session_factory() as session:
            data = await session.execute(statement)
            return data.scalars().all()

    async def create_discord_verification(self, user: discordVerificationCreate):
        """
        Create a new discord verification in the database.

        Parameters:
            user: The discord verification to create in the database.

        Returns:
            The created discord verification.
        """
        async with self.session_factory() as session:
            db_verification = discordVerification.from_orm(user)
            session.add(db_verification)
            await session.commit()
            await session.refresh(db_verification)
            return db_verification
