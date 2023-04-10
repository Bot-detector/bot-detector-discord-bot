from sqlalchemy import Column, ForeignKeyConstraint, Index, Integer
from sqlalchemy.dialects.mysql import TEXT, TINYINT

from src.core.database.session import Base


class DiscordVerification(Base):
    __tablename__ = "discordVerification"
    __table_args__ = (
        ForeignKeyConstraint(
            ["Player_id"],
            ["playerdata.Players.id"],
            ondelete="RESTRICT",
            onupdate="RESTRICT",
            name="FK_real_players",
        ),
        ForeignKeyConstraint(
            ["token_used"],
            ["playerdata.Tokens.id"],
            ondelete="RESTRICT",
            onupdate="RESTRICT",
            name="FK_token_used",
        ),
        Index("FK_real_players", "Player_id"),
        Index("FK_token_used", "token_used"),
        Index("idx_discordID_playerID", "Discord_id", "Player_id", unique=True),
    )

    id = Column("Entry", Integer, primary_key=True)
    discord_id = Column("Discord_id", Integer, nullable=False)
    player_id = Column("Player_id", Integer, nullable=False)
    primary_rsn = Column("primary_rsn", TINYINT, server_default="0")
    code = Column("Code", TEXT, nullable=False)
    verified_status = Column("Verified_status", TINYINT, server_default="0")
    token_used = Column("token_used", Integer, server_default=None)
