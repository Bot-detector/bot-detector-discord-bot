from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import TEXT, TINYINT

from src.core.database import Base


class DiscordVerification(Base):
    __tablename__ = "discordVerification"

    Entry = Column("Entry", Integer, primary_key=True)
    Discord_id = Column("Discord_id", Integer)
    Player_id = Column("Player_id", Integer)
    primary_rsn = Column("primary_rsn", TINYINT)
    Code = Column("Code", TEXT)
    verified_status = Column("verified_status", TINYINT)
    token_used = Column("token_used", Integer, server_default=None)
