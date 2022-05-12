import logging

import discord
from discord.ext.commands import Bot
import aiohttp
from src import config
from src.cogs import fun_commands

logger = logging.getLogger(__name__)

activity = discord.Game("OSRS", type=discord.ActivityType.watching)
allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)


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
bot.add_cog(fun_commands.funCommands(bot))

# default events
@bot.event
async def on_ready():
    global Session
    logger.info(f"We have logged in as {bot.user}")
    async with aiohttp.ClientSession() as session:
        Session = session


@bot.event
async def on_connect():
    logger.info("Bot connected successfully.")


@bot.event
async def on_disconnect():
    logger.info("Bot disconnected.")
