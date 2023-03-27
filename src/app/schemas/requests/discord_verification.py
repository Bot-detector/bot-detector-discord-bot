from pydantic import BaseModel


class DiscordVerificationCreateRequest(BaseModel):
    discord_id: int
    player_id: int
