import logging
import aiohttp

import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from src import config
from inspect import cleandoc
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class Stats(BaseModel):
    total_bans: int
    total_real_players: int
    total_accounts: int

class projectStatsCommands(Cog):
    def __init__(self, bot: discord.Client) -> None:
        """
        Initialize the modCommands class.
        :param bot: The discord bot client.
        """
        self.bot = bot

    async def get_active_installs(self) -> int:
        session: aiohttp.ClientSession = self.bot.Session
        url = "https://api.runelite.net/runelite/pluginhub"

        response = await session.get(url)

        data = None
        if response.ok:
            data: dict = await response.json()
            data = data.get("bot-detector")
        return data

    async def create_stats_embed(
        self,
        total_accounts: int,
        confirmed_players: int,
        confirmed_bans: int,
        active_installs: int,
    ):
        embed = discord.Embed(title="Bot Detector Plugin", color=0x00FF00)
        embed.add_field(
            name="= Project Stats =",
            inline=False,
            value=cleandoc(
                f"""
                Players Analyzed: {total_accounts:,}
                Confirmed Players: {confirmed_players:,}
                Total Bans: {confirmed_bans:,}
                Active Installs: {active_installs:,}
            """
            )
        )

        embed.set_thumbnail(
            url="https://user-images.githubusercontent.com/5789682/117360948-60a24f80-ae87-11eb-8a5a-7ba57f85deb2.png"
        )
        return embed

    @commands.hybrid_command()
    async def stats(self, ctx: Context):
        logger.debug(f"{ctx.author.name=}, {ctx.author.id=}, Requesting stats")
        project_stats: dict = await config.api.get_project_stats()
        logger.info(f"{project_stats=}")

        # validate stats
        stats = Stats(**project_stats)
        
        active_installs = await self.get_active_installs()
        active_installs = active_installs if active_installs else ''
        logger.info(f"{active_installs=}")

        embed = discord.Embed(title="Bot Detector Plugin", color=0x00FF00)
        embed.add_field(
            name="= Project Stats =",
            inline=False,
            value=cleandoc(
                f"""
                Players Analyzed: {stats.total_accounts:,}
                Confirmed Players: {stats.total_real_players:,}
                Total Bans: {stats.total_bans:,}
                Active Installs: {active_installs:,}
            """
            )
        )

        embed.set_thumbnail(
            url="https://user-images.githubusercontent.com/5789682/117360948-60a24f80-ae87-11eb-8a5a-7ba57f85deb2.png"
        )
        await ctx.reply(embed=embed)
        return
