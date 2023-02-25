from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import TINYINT, DATETIME
from datetime import datetime

from src.core.database import Base


class DiscordEventParticipant(Base):
    __tablename__ = "discordEventParticipant"

    id = Column("id", Integer, primary_key=True)
    created_at = Column("created_at", DATETIME, default=datetime.utcnow)
    updated_at = Column("updated_at", DATETIME, onupdate=datetime.utcnow)
    event_id = Column("event_id", Integer)
    verification_id = Column("verification_id", Integer)
    participating = Column("participating", TINYINT)
