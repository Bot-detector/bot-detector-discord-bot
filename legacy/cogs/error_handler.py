import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context
import traceback
import sys
import aiohttp
from discord import Webhook
from src import config

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
        print("error", error)
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

        if isinstance(error, commands.DisabledCommand):
            await ctx.reply(f"{ctx.command} has been disabled.")
        elif isinstance(error, commands.MissingAnyRole):
            logger.debug(f"user: {ctx.author}, {error}")
            await ctx.reply("You are missing at least one of the required roles")
        elif isinstance(error, commands.MissingRequiredArgument):
            logger.debug(f"user: {ctx.author}, {error}")
            await ctx.reply(str(error))
        elif isinstance(error, commands.CheckFailure):
            await ctx.reply(
                "You can only message in the allowed channels, in the bot detector guild."
            )
        else:
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )

            logger.error({"error": error})
            await ctx.send("An error occured.")

            if config.WEBHOOK:
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(config.WEBHOOK, session=session)
                    error_traceback = traceback.format_exception(
                        type(error), error, error.__traceback__
                    )
                    error_message = (
                        f"`{ctx.author}` running `{ctx.command}` caused `{error.__class__.__name__}`\n"
                        f"Message Link: {ctx.message.jump_url}\n"
                        f"```{''.join(error_traceback)}```"
                    )
                    error_message = "".join(error_message)

                    for secret in config.SECRETS:
                        error_message = error_message.replace(secret, "***")
                    await webhook.send(error_message, username="bd-error")
