from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    Index,
    Integer,
)
from sqlalchemy.dialects.mysql import DATETIME, TINYINT
from sqlalchemy.orm import relationship

from src.core.database.session import Base


class DiscordEventParticipant(Base):
    __tablename__ = "discordEventParticipant"
    __table_args__ = (
        ForeignKeyConstraint(
            ["event_id"], ["discordEvent.id"], name="discordEventParticipant_ibfk_1"
        ),
        ForeignKeyConstraint(
            ["verification_id"],
            ["discordVerification.Entry"],
            name="discordEventParticipant_ibfk_2",
        ),
        Index("unique_participant", "event_id", "verification_id", unique=True),
        Index("verification_id", "verification_id"),
    )

    id = Column("id", Integer, primary_key=True)
    created_at = Column("created_at", DATETIME, default=datetime.utcnow)
    updated_at = Column("updated_at", DATETIME, onupdate=datetime.utcnow)
    event_id = Column("event_id", Integer)
    verification_id = Column("verification_id", Integer)
    participating = Column("participating", TINYINT, server_default=1)

    event = relationship("DiscordEvent", back_populates="discordEventParticipant")
    verification = relationship(
        "DiscordVerification", back_populates="discordEventParticipant"
    )
