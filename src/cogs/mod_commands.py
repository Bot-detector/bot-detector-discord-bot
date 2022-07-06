import logging

import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context

logger = logging.getLogger(__name__)


class modCommands(Cog):
    def __init__(self, bot: discord.Client) -> None:
        """
        Initialize the modCommands class.
        :param bot: The discord bot client.
        """
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx: Context):
        logger.debug(f"{ctx.author}, is using warn.")
        embed = discord.Embed(title=f"WARNING", color=0xFF0000)
        name = "= WARNING MESSAGE ="
        value = "**Do not attempt to contact the Jmods or Admins in any channel regarding the status of your Runescape account: Doing so will result in an automatic permanent ban.**\n**This is your only warning.**\n"
        url = "https://user-images.githubusercontent.com/5789682/117366156-59327480-ae8e-11eb-8b08-6cf815d8a36e.png"
        embed.add_field(name=name, value=value, inline=False)
        embed.set_thumbnail(url=url)
        ctx.send(embed=embed)

    # i don't think we want an update_all_roles command
    # i don't think we want an update_faq command
