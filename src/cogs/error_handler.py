import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context
import traceback
import sys

logger = logging.getLogger(__name__)


class errorHandler(commands.Cog):
    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound,)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            logger.debug(f"ignored: {error}")
            return

        if isinstance(error, commands.MissingAnyRole):
            logger.debug(f"user: {ctx.author}, {error}")
            await ctx.reply("You are missing at least one of the required roles")
        elif isinstance(error, commands.MissingRequiredArgument):
            logger.debug(f"user: {ctx.author}, {error}")
            await ctx.reply(str(error))
        else:
            await ctx.reply("An error occured.")
            logger.error(error)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
