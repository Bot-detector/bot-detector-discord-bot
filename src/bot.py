import logging

import aiohttp
import discord
from discord.ext.commands import Bot

from src import config
from src.cogs.fun_commands import funCommands
from src.cogs.bot_detective_commands import botDetectiveCommands
from src.cogs.error_handler import errorHandler
from src.cogs.rsn_linking_commands import rsnLinkingCommands
from src.cogs.mod_commands import modCommands
from src.cogs.project_stats import projectStatsCommands
from src.cogs.player_stats_commands import playerStatsCommands
from src.cogs.map_commands import mapCommands

logger = logging.getLogger(__name__)

activity = discord.Game("OSRS", type=discord.ActivityType.watching)
allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
intents = discord.Intents(
    messages=True, guilds=True, members=True, reactions=True, message_content=True
)


bot: discord.Client = Bot(
    allowed_mentions=allowed_mentions,
    command_prefix=config.COMMAND_PREFIX,
    description="busting bots",
    case_insensitive=True,
    activity=activity,
    intents=intents,
)

# register our own commands, these should be in the cogs folder
# bot.add_cog(className(bot))

# default events
@bot.event
async def on_ready():
    logger.info(f"We have logged in as {bot.user}")
    bot.Session = aiohttp.ClientSession()
    await bot.add_cog(funCommands(bot))
    await bot.add_cog(botDetectiveCommands(bot))
    await bot.add_cog(errorHandler(bot))
    await bot.add_cog(rsnLinkingCommands(bot))
    await bot.add_cog(modCommands(bot))
    await bot.add_cog(projectStatsCommands(bot))
    await bot.add_cog(playerStatsCommands(bot))
    await bot.add_cog(mapCommands(bot))


@bot.event
async def on_connect():
    logger.info("Bot connected successfully.")
    logger.info(f"{config.COMMAND_PREFIX=}")


@bot.event
async def on_disconnect():
    logger.info("Bot disconnected.")
