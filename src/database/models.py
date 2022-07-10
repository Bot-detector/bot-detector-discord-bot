from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import TEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

# generated with sqlacodegen
Base = declarative_base()
metadata = Base.metadata


class discordVerification(Base):
    __tablename__ = "discordVerification"

    id = Column("Entry", Integer, primary_key=True)
    discord_id = Column("Discord_id", Integer)
    player_id = Column("Player_id", Integer)
    primary_name = Column("primary_rsn", TINYINT, server_default=0)
    code = Column("Code", TEXT)
    status = Column("verified_status", TINYINT, server_default=0)
    token = Column("token_used", Integer, server_default=None)
