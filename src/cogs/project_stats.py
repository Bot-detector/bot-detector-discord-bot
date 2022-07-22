import logging
import aiohttp

import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from src import config
from inspect import cleandoc

logger = logging.getLogger(__name__)


class projectStatsCommands(Cog):
    def __init__(self, bot: discord.Client) -> None:
        """
        Initialize the modCommands class.
        :param bot: The discord bot client.
        """
        self.bot = bot

    async def get_active_installs(self) -> int:
        session: aiohttp.ClientSession = self.bot.Session
        url = "https://api.runelite.net/runelite-1.8.27/pluginhub"

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
                Confirmed Players: {(confirmed_players):,}
                Total Bans: {confirmed_bans:,}
                Active Installs: {active_installs:,}
            """
            ),
        )

        embed.set_thumbnail(
            url="https://user-images.githubusercontent.com/5789682/117360948-60a24f80-ae87-11eb-8a5a-7ba57f85deb2.png"
        )
        return embed

    @commands.command()
    async def stats(self, ctx: Context):
        project_stats: dict = await config.api.get_project_stats()
        logger.debug(f"{project_stats=}")

        active_installs = await self.get_active_installs()
        logger.debug(f"{active_installs=}")

        embed = await self.create_stats_embed(
            total_accounts=project_stats.get("total_accounts"),
            confirmed_players=project_stats.get("total_real_players"),
            confirmed_bans=project_stats.get("total_bans"),
            active_installs=active_installs,
        )
        await ctx.reply(embed=embed)
        return
