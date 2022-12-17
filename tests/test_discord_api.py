import pytest
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select
from typing import List, Optional

from src.database.models import discordVerification, discordVerificationCreate
from src.services import DiscordAPI


class PaginationParams(BaseModel):
    limit: int = Field(default=10, gt=0, lt=100)
    offset: int = Field(default=0, ge=0)
    
@pytest.mark.asyncio
async def test_get_discord_verifications(session_factory, test_discord_verification):
    async with session_factory() as session:
        discord_api = DiscordAPI(session_factory)
        pagination_params = PaginationParams(offset=0, limit=10)

        # Test getting all discord verifications
        result = await discord_api.get_discord_verifications(pagination_params)
        assert result == [test_discord_verification]

        # Test getting discord verifications by entry
        result = await discord_api.get_discord_verifications(
            pagination_params, entry=test_discord_verification.Entry
        )
        assert result == [test_discord_verification]

        # Test getting discord verifications by player id
        result = await discord_api.get_discord_verifications(
            pagination_params, player_id=test_discord_verification.Player_id
        )
        assert result == [test_discord_verification]

        # Test getting discord verifications by discord id
        result = await discord_api.get_discord_verifications(
            pagination_params, discord_id=test_discord_verification.Discord_id
        )
        assert result == [test_discord_verification]