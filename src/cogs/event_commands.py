import logging
import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from src import config
from src.utils.checks import VERIFIED_PLAYER_ROLE, DISCORD_STAFF, OWNER_ROLE
from typing import Literal
from src.database.api import discordApi

logger = logging.getLogger(__name__)
discord_api = discordApi()


class eventCommands(Cog):
    def __init__(self, bot: discord.Client) -> None:
        """
        Initialize the playerStatsCommands class.
        :param bot: The discord bot client.
        """
        self.bot = bot

    @commands.hybrid_command(name="event", description="join or leave a discord event.")
    @commands.has_any_role(VERIFIED_PLAYER_ROLE)  # verified
    async def _event(
        self, ctx: Context, action: Literal["join", "leave"], event_name: str
    ):
        logger.debug(
            f"{ctx.author.name=}, {ctx.author.id=}, /event {action} {event_name}"
        )
        # get player
        linked_accounts = await discord_api.get_verified_player(
            discord_id=ctx.author.id, is_verified=True
        )

        # check if player is linked
        if not linked_accounts:
            await ctx.reply("Your Discord account is not linked to a game account.")
            return

        # get event
        event = await discord_api.get_event(event_name, active=True)
        if not event:
            await ctx.send(f"Could not find an event with the name '{event_name}'.")
            return
        event = event[0]

        # get event participants
        event_participants = list()
        for account in linked_accounts:
            participant = await discord_api.get_event_participants(
                event_id=event["id"],
                verification_id=account["Entry"],
                participating=True,
            )
            if participant:
                event_participants.append(participant)

        # handle join/leave
        match action:
            case "join":
                if event_participants:
                    await ctx.send("You have already joined this event.")
                    return
                # join event
                for account in linked_accounts:
                    await discord_api.join_event(
                        event_id=event["id"], verification_id=account["Entry"]
                    )
                await ctx.send("Successfully joined the event.")
            case "leave":
                if not event_participants:
                    await ctx.send("You have not joined this event.")
                    return
                # leave event
                for account in linked_accounts:
                    await discord_api.leave_event(
                        event_id=event["id"], verification_id=account["Entry"]
                    )
                await ctx.send("Successfully left the event.")

    @commands.hybrid_command()
    @commands.has_any_role(DISCORD_STAFF, OWNER_ROLE)
    async def create_event(self, ctx: Context, event_name: str):
        """
        Creates a new discord event.

        Args:
            event_name (str): The name of the event to create.
        """
        # create event
        try:
            event = await discord_api.create_event(event_name=event_name)
        except ValueError:
            await ctx.reply("an event with that name already exists")
            return

        event = event[0]
        await ctx.reply(f"Successfully created the event {event['event_name']}.")
        return

    @commands.hybrid_command(name="delete_event")
    @commands.has_any_role(DISCORD_STAFF, OWNER_ROLE)
    async def delete_event(self, ctx: Context, event_name: str):
        """
        Deletes a discord event.

        Args:
            event_name (str): The name of the event to delete.
        """
        # delete event
        event = await discord_api.get_event(event_name, active=True)
        if not event:
            await ctx.reply("an event with that name does not exist")
            return

        event = event[0]
        await discord_api.update_event(
            event_id=event["id"], event_name=event["event_name"], active=False
        )

        await ctx.reply("delete event")
        return
