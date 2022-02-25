import asyncio
import logging

import aiohttp
import discord

from src import config

logger = logging.getLogger(__name__)

activity = discord.Game("OSRS", type=discord.ActivityType.watching)
allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)

bot = discord.ext.commands.Bot(
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


@bot.event
async def on_connect():
    logger.info("Bot connected successfully.")


@bot.event
async def on_disconnect():
    logger.info("Bot disconnected.")


async def startup():
    bot.loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession() as session:
        bot.session = session
        with open("error.log", "w+") as error_file:
            bot.error_file = error_file
            await bot.start(config.TOKEN)

    logger.info("Bot is going night-night.")
    await bot.close()


asyncio.run(startup())
