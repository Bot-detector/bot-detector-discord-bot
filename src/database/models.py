from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import TEXT, TINYINT, VARCHAR, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# generated with sqlacodegen
Base = declarative_base()
metadata = Base.metadata


class discordVerification(Base):
    __tablename__ = "discordVerification"

    Entry = Column("Entry", Integer, primary_key=True)
    Discord_id = Column("Discord_id", Integer)
    Player_id = Column("Player_id", Integer)
    primary_rsn = Column("primary_rsn", TINYINT)
    Code = Column("Code", TEXT)
    verified_status = Column("verified_status", TINYINT)
    token_used = Column("token_used", Integer, server_default=None)


class discordEvent(Base):
    __tablename__ = "discordEvent"
    id = Column("id", Integer, primary_key=True)
    created_at = Column("created_at", DATETIME, default=datetime.utcnow)
    updated_at = Column("updated_at", DATETIME, onupdate=datetime.utcnow)
    event_name = Column("event_name", VARCHAR(50), unique=True)
    active = Column("active", TINYINT, default=1)


class discordEventParticipant(Base):
    __tablename__ = "discordEventParticipant"

    id = Column("id", Integer, primary_key=True)
    created_at = Column("created_at", DATETIME, default=datetime.utcnow)
    updated_at = Column("updated_at", DATETIME, onupdate=datetime.utcnow)
    event_id = Column("event_id", Integer)
    verification_id = Column("verification_id", Integer)
    participating = Column("participating", TINYINT)
