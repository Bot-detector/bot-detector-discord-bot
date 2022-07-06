import imp
import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context
from src.utils import string_processing
from src import config

logger = logging.getLogger(__name__)


class rsnLinkingCommands(commands.Cog):
    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot

    @commands.command()
    async def link(self, ctx: Context, *, name: str = None):
        # check if a name is given
        if not name:
            await ctx.send(
                "Please specify the RSN of the account you'd wish to link. !link <RSN>"
            )
            return
        # check if the name is valid
        if not string_processing.is_valid_rsn(name):
            await ctx.send(f"{name} isn't a valid Runescape user name.")
            return

        # TODO: check if player exists on the bot detector api
        player = await config.api.get_player(name=name)
        if not player:
            embed = discord.Embed(title=f"User Not Found:", color=0xFF0000)
            embed.add_field(
                name="Status:",
                value=f"No reports exist from specified player.",
                inline=False,
            )
            embed.add_field(
                name="Next Steps:",
                value=f"Please install the Bot-Detector Plugin on RuneLite if you have not done so.\n\nIf you have the plugin installed, you will need to disable Anonymous Reporting for us to be able to !link your account.",
                inline=False,
            )
            embed.set_thumbnail(
                url="https://user-images.githubusercontent.com/5789682/117361316-e1f9e200-ae87-11eb-840b-3bad75e80ff6.png"
            )
            await ctx.send(embed=embed)
        