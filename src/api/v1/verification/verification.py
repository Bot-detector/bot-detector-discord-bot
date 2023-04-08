from random import randint
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories.discord_verification import DiscordVerificationRepository
from src.app.schemas.requests.discord_verification import (
    DiscordVerificationCreateRequest,
)
from src.core.database.session import get_session
from src.core.fastapi.dependencies.auth import authenticate_user

router = APIRouter()


async def get_discord_verification_repository(
    session: AsyncSession = Depends(get_session),
):
    return DiscordVerificationRepository(session)


@router.post("/")
async def create_discord_verification(
    verification_data: DiscordVerificationCreateRequest,
    usr: bool = Depends(authenticate_user),
    repo: DiscordVerificationRepository = Depends(get_discord_verification_repository),
):
    code = str(randint(1000, 9999))
    verification_id = await repo.create(
        verification_data.discord_id,
        verification_data.player_id,
        code,
    )
    return {"verification_id": verification_id}


@router.get("/")
async def read_discord_verification(
    verification_id: Annotated[int | None, Query()],
    player_id: Annotated[int | None, Query()],
    usr: bool = Depends(authenticate_user),
    repo: DiscordVerificationRepository = Depends(get_discord_verification_repository),
):
    verification = await repo.read(verification_id, player_id)
    return verification


@router.put("/")
async def update_discord_verification(
    verification_id: Annotated[int, Query()],
    verified_status: Annotated[bool, Query()],
    usr: bool = Depends(authenticate_user),
    repo: DiscordVerificationRepository = Depends(get_discord_verification_repository),
):
    await repo.update(verification_id, verified_status)
    return {"message": "Verification updated successfully"}


@router.delete("/")
async def delete_discord_verification(
    verification_id: Annotated[int, Query(...)],
    usr: bool = Depends(authenticate_user),
    repo: DiscordVerificationRepository = Depends(get_discord_verification_repository),
):
    await repo.delete(verification_id)
    return {"message": "Verification deleted successfully"}
