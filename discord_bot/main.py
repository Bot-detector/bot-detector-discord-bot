import logging
import random

from discord import Activity, ActivityType, Intents
from discord.ext import commands
from discord.ext.commands import Context

# Import your logging configuration
import core.logging
from core.config import CONFIG

logger = logging.getLogger(__name__)

intents = Intents.default()
bot = commands.Bot(command_prefix=CONFIG.COMMAND_PREFIX, intents=intents)
bot.load_extension("app.controllers")


@bot.event
async def on_ready():
    await bot.change_presence(activity=Activity(type=ActivityType.playing, name="OSRS"))
    logger.info(f"Logged in as {bot.user.name}")


@bot.event
async def on_connect():
    logger.info("Bot connected successfully.")
    logger.info(f"{CONFIG.COMMAND_PREFIX=}")


@bot.event
async def on_disconnect():
    logger.info("Bot disconnected.")


@bot.listen
async def on_command(ctx: Context):
    _log = {"author": ctx.author}
    _log["command"] = "text" if ctx.interaction is None else "slash"
    logger.info(_log)

    responses = [
        "Slash commands are faster and easier to use!",
        "Did you know that you can do everything with slash commands?",
        "Slash commands help keep the chat clean and organized.",
        "Try using slash commands for a smoother experience.",
        "Slash commands are the future of Discord. Give them a try!",
    ]

    if ctx.interaction is None:
        if random.randint(0, 100) == 0:
            await ctx.reply(random.choice(responses))


if __name__ == "__main__":
    bot.run(CONFIG.TOKEN)
