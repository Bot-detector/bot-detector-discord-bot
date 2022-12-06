from src.database.database import DISCORD_ENGINE, sqlalchemy_result
from src.database.models import (
    discordEventParticipant,
    discordEvent,
    discordVerification,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import (
    Select,
    select,
    insert,
    Insert,
    delete,
    Delete,
    Update,
    update,
    and_,
)
from typing import Optional, Dict, Any


class discordApi:
    async def create_event(self, event_name: str) -> dict:
        """Args:
        event_name (str): The name of the event to create.

        Returns:
            dict: A dictionary containing the created event data.
        """
        # create new discord event
        values = dict(event_name=event_name, active=1)
        sql: Insert = insert(discordEvent).values(values)

        # check if event with given name already exists
        event = await self.get_event(event_name)

        if event:
            raise ValueError("event already exists")

        async with DISCORD_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                result = await session.execute(sql)

        # get created event data
        sql: Select = select(discordEvent)
        sql = sql.where(discordEvent.id == result.inserted_primary_key[0])

        async with DISCORD_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                data = await session.execute(sql)

        data = sqlalchemy_result(data)
        return data.rows2dict()

    async def update_event(self, event_id: int, event_name: str, active: bool) -> dict:
        """Updates a discord event.

        Args:
            event_id (int): The ID of the event to update.
            event_name (str): The new name of the event.
            active (bool): Whether the event is active or not.

        Returns:
            dict: A dictionary containing the updated event data.
        """
        # Update the event record in the database
        sql: Update = update(discordEvent)
        sql = sql.where(discordEvent.id == event_id)
        sql = sql.values(event_name=event_name, active=active)

        async with DISCORD_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                await session.execute(sql)

        # Fetch the updated event record from the database
        sql: Select = select(discordEvent)
        sql = sql.where(discordEvent.id == event_id)

        async with DISCORD_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                data = await session.execute(sql)

        data = sqlalchemy_result(data)
        return data.rows2dict()

    async def get_event(self, event_name: str, active: bool = None) -> dict:
        """Fetches a discord event by event name.

        Args:
            event_name (str): The name of the event to fetch.

        Returns:
            dict: A dictionary containing the event data.
        """
        sql: Select = select(discordEvent)
        sql = sql.where(discordEvent.event_name == event_name)
        if active is not None:
            sql = sql.where(discordEvent.active == active)

        async with DISCORD_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                data = await session.execute(sql)

        data = sqlalchemy_result(data)
        return data.rows2dict()

    async def join_event(
        self, event_id: str, verification_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Adds a verified player to the list of participants for a discord event.

        Args:
            event_id (str): The ID of the event to join.
            verification_id (int): The ID of the verified player who is joining the event.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the data for the newly created event participant, or None if the player is already participating in the event.
        """
        # get the event participant
        event_participant = await self.get_event_participants(
            event_id=event_id, 
            verification_id=verification_id
        )
        
        exists = False

        # check if participant is already present
        if event_participant:
            event_participant:dict = event_participant[0]
            participating = event_participant.get('participating')
            if participating == False:
                exists = True
            else:
                return None

        if exists:
            # update player status
            sql: Update = update(discordEventParticipant)
            sql = sql.where(discordEventParticipant.event_id == event_id)
            sql = sql.where(discordEventParticipant.verification_id == verification_id)
            sql = sql.values(participating=True)
        else:
            # add player to event participants
            sql: Insert = insert(discordEventParticipant)
            sql = sql.values(event_id=event_id, verification_id=verification_id)

        async with DISCORD_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                await session.execute(sql)

        # fetch newly created event participant
        event_participan = await self.get_event_participants(
            event_id=event_id, verification_id=verification_id
        )
        return event_participan

    async def leave_event(
        self, event_id: int, verification_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Removes a verified player from the list of participants for a discord event.

        Args:
            event_id (int): The ID of the event to leave.
            verification_id (int): The ID of the verified player who is leaving the event.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the updated data for the discord event participant, if it exists.
        """
        sql: Update = update(discordEventParticipant)
        sql = sql.where(
            and_(
                (discordEventParticipant.event_id == event_id),
                (discordEventParticipant.verification_id == verification_id),
            )
        ).values(participating=False)

        # Use the statement to update the record in the database
        async with DISCORD_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                await session.execute(sql)

        return await self.get_event_participants(event_id, verification_id)

    async def get_verified_player(
        self, discord_id: str = None, player_id: int = None, is_verified: bool = None
    ) -> dict:
        """Fetches a verified player by their Discord ID or player ID.

        Args:
            discord_id (str, optional): The Discord ID of the player to fetch.
            player_id (int, optional): The player ID of the player to fetch.

        Returns:
            dict: A dictionary containing the player's data.
        """
        if discord_id == player_id == None:
            return None

        sql: Select = select(discordVerification)
        if is_verified is not None:
            sql = sql.where(discordVerification.verified_status == is_verified)

        if discord_id:
            sql = sql.where(discordVerification.Discord_id == discord_id)

        if player_id:
            sql = sql.where(discordVerification.Player_id == player_id)

        async with DISCORD_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                data = await session.execute(sql)

        data = sqlalchemy_result(data)
        return data.rows2dict()

    async def get_event_participants(
        self, event_id: str, verification_id: int = None, participating: bool = None
    ) -> dict:
        """Fetches the participants of a discord event.

        Args:
            event_id (str): The ID of the event to fetch participants for.
            verification_id (int): The ID of the verified player to filter by.

        Returns:
            dict: A dictionary containing the event participants data.
        """
        sql: Select = select(discordEventParticipant)
        sql = sql.where(discordEventParticipant.event_id == event_id)

        if verification_id:
            sql = sql.where(discordEventParticipant.verification_id == verification_id)

        if participating:
            sql = sql.where(discordEventParticipant.participating == participating)

        async with DISCORD_ENGINE.get_session() as session:
            session: AsyncSession = session
            async with session.begin():
                data = await session.execute(sql)

        data = sqlalchemy_result(data)
        return data.rows2dict()
