import asyncio
import logging
import random
from typing import Optional, Sequence

import discord
from discord import Activity, ActivityType, Intents
from discord.ext import commands
from discord.ext.commands import Context

# Import your logging configuration
import core.logging
from core.config import CONFIG
from enum import Enum

logger = logging.getLogger(__name__)


class SyncOption(str, Enum):
    GLOBAL = "~"
    CURRENT_GUILD = "*"
    CLEAR_COMMANDS = "^"


class MyBot(commands.Bot):
    async def setup_hook(self):
        await bot.load_extension("app.controllers")


intents = Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
bot = MyBot(command_prefix=CONFIG.COMMAND_PREFIX, intents=intents)


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


@bot.listen("on_command")
async def on_command(ctx: Context):
    _log = {
        "author_id": ctx.author.id,
        "author_name": ctx.author.name,
        "guild": ctx.guild.name if ctx.guild else "DM",
    }
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


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
    ctx: Context,
    guilds: Sequence[discord.Object] = (),
    spec: Optional[SyncOption] = None,
) -> None:
    logger.debug(f"{ctx.author.name=}, {ctx.author.id=}, Requesting sync, {spec=}")

    bot: MyBot = ctx.bot
    if not guilds:
        match spec:
            case SyncOption.GLOBAL:
                synced = await bot.tree.sync(guild=ctx.guild)
                await ctx.send(f"Synced {len(synced)} commands globally")
            case SyncOption.CURRENT_GUILD:
                bot.tree.copy_global_to(guild=ctx.guild)
                synced = await bot.tree.sync(guild=ctx.guild)
                await ctx.send(f"Synced {len(synced)} commands to the current guild")
            case SyncOption.CLEAR_COMMANDS:
                bot.tree.clear_commands(guild=ctx.guild)
                await bot.tree.sync(guild=ctx.guild)
                await ctx.send("Cleared all commands for the current guild")
            case None:
                synced = await bot.tree.sync()
                await ctx.send(f"Synced {len(synced)} commands globally")
    else:
        tasks = [bot.tree.sync(guild=guild) for guild in guilds]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        synced = [res for res in results if isinstance(res, list)]
        synced_count = len(synced)
        await ctx.send(f"Synced the tree to {synced_count}/{len(guilds)} guilds.")


if __name__ == "__main__":
    bot.run(CONFIG.TOKEN)
