import logging
from typing import Literal, Optional

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context, Greedy

logger = logging.getLogger(__name__)

activity = discord.Game("OSRS", type=discord.ActivityType.watching)
allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
intents = discord.Intents(
    messages=True, guilds=True, members=True, reactions=True, message_content=True
)


bot: discord.Client = Bot(
    allowed_mentions=allowed_mentions,
    command_prefix="",  # TODO: prefix
    description="busting bots",
    case_insensitive=True,
    activity=activity,
    intents=intents,
)


# @bot.check
# async def globally_block_dms(ctx: Context):
#     return ctx.guild is not None


# @bot.check
# async def globally_check_channel(ctx: Context):
#     return await checks.is_allowed_channel(ctx)


# @bot.event
# async def setup_hook():
#     await bot.add_cog(funCommands(bot))
#     await bot.add_cog(botDetectiveCommands(bot))
#     await bot.add_cog(errorHandler(bot))
#     await bot.add_cog(rsnLinkingCommands(bot))
#     await bot.add_cog(modCommands(bot))
#     await bot.add_cog(projectStatsCommands(bot))
#     await bot.add_cog(playerStatsCommands(bot))
#     await bot.add_cog(mapCommands(bot))
#     await bot.add_cog(eventCommands(bot))


# # default events
# @bot.event
# async def on_ready():
#     logger.info(f"We have logged in as {bot.user}")
#     bot.Session = aiohttp.ClientSession()
#     await bot.tree.sync()


# @bot.event
# async def on_connect():
#     logger.info("Bot connected successfully.")
#     logger.info(f"{config.COMMAND_PREFIX=}")


# @bot.event
# async def on_disconnect():
#     logger.info("Bot disconnected.")


# @bot.command()
# @commands.guild_only()
# @commands.is_owner()
# async def sync(
#     ctx: Context,
#     guilds: Greedy[discord.Object],
#     spec: Optional[Literal["~", "*", "^"]] = None,
# ) -> None:
#     logger.debug(f"{ctx.author.name=}, {ctx.author.id=}, Requesting sync, {spec=}")
#     if not guilds:
#         if spec == "~":
#             synced = await ctx.bot.tree.sync(guild=ctx.guild)
#         elif spec == "*":
#             ctx.bot.tree.copy_global_to(guild=ctx.guild)
#             synced = await ctx.bot.tree.sync(guild=ctx.guild)
#         elif spec == "^":
#             ctx.bot.tree.clear_commands(guild=ctx.guild)
#             await ctx.bot.tree.sync(guild=ctx.guild)
#             synced = []
#         else:
#             synced = await ctx.bot.tree.sync()

#         await ctx.send(
#             f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
#         )
#         return

#     ret = 0
#     for guild in guilds:
#         try:
#             await ctx.bot.tree.sync(guild=guild)
#         except discord.HTTPException:
#             pass
#         else:
#             ret += 1

#     await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
