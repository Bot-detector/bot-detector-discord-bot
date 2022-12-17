from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import TEXT, TINYINT, VARCHAR, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import string
import random
from sqlmodel import SQLModel
from typing import Optional
from sqlmodel import Field

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
    __tablename__ = 'discordEvent'
    id = Column('id', Integer, primary_key=True)
    created_at = Column('created_at', DATETIME, default=datetime.utcnow)
    updated_at = Column('updated_at', DATETIME, onupdate=datetime.utcnow)
    event_name = Column('event_name', VARCHAR(50), unique=True)
    active = Column('active', TINYINT, default=1)

class discordEventParticipant(Base):
    __tablename__ = "discordEventParticipant"

    id = Column("id", Integer, primary_key=True)
    created_at = Column('created_at', DATETIME, default=datetime.utcnow)
    updated_at = Column('updated_at', DATETIME, onupdate=datetime.utcnow)
    event_id = Column("event_id", Integer)
    verification_id = Column("verification_id", Integer)
    participating = Column("participating", TINYINT)

#############################################################################

def random_code_factory() -> str:
    letters = string.digits
    return "".join(random.choice(letters) for i in range(4))


class discordVerificationBase(SQLModel):
    Discord_id: str
    Player_id: int

    primary_rsn: Optional[int] = Field(default=0)
    verified_status: Optional[int] = Field(default=0)
    token_used: Optional[int] = Field(default=None)


class discordVerification(discordVerificationBase, table=True):
    __tablename__ = "discordVerification"

    Entry: Optional[int] = Field(default=None, primary_key=True)
    Code: str = Field(default_factory=random_code_factory, nullable=False)


class discordVerificationCreate(discordVerificationBase):
    pass


class discordVerificationRead(discordVerificationBase):
    Entry: int
    Code: str

# TODO: split read & write
class discordEvent(SQLModel):
    __tablename__ = 'discordEvent'

    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow)
    updated_at: datetime = Field(onupdate=datetime.utcnow)
    event_name: str = Field(unique=True)
    active: Optional[int] = Field(default=1)

class discordEventParticipant(SQLModel):
    __tablename__ = "discordEventParticipant"

    id: int = Field(primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow)
    updated_at: datetime = Field(onupdate=datetime.utcnow)
    event_id: int
    verification_id: int
    participating: Optional[int] = Field(default=0)