import logging

import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from src.utils.checks import DISCORD_STAFF, OWNER_ROLE, VERIFICATION_STAFF
from src import config

logger = logging.getLogger(__name__)


class modCommands(Cog):
    def __init__(self, bot: discord.Client) -> None:
        """
        Initialize the modCommands class.
        :param bot: The discord bot client.
        """
        self.bot = bot

    def _batch(self, iterable, n=1) -> list:
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx : min(ndx + n, l)]

    @commands.hybrid_command()
    @commands.has_any_role(DISCORD_STAFF, OWNER_ROLE)
    async def warn(self, ctx: Context):
        """"""
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": f"is using warn",
        }
        logger.debug(debug)

        embed = discord.Embed(title=f"WARNING", color=0xFF0000)
        name = "= WARNING MESSAGE ="
        value = "**Do not attempt to contact the Jmods or Admins in any channel regarding the status of your Runescape account: Doing so will result in an automatic permanent ban.**\n**This is your only warning.**\n"
        url = "https://user-images.githubusercontent.com/5789682/117366156-59327480-ae8e-11eb-8b08-6cf815d8a36e.png"
        embed.add_field(name=name, value=value, inline=False)
        embed.set_thumbnail(url=url)
        await ctx.send(embed=embed)

    # i don't think we want an update_all_roles command
    # i don't think we want an update_faq command

    @commands.hybrid_command()
    @commands.has_any_role(DISCORD_STAFF, VERIFICATION_STAFF, OWNER_ROLE)
    async def admin_linked(self, ctx: Context, discord_id:str):
        """Sends a message to the user with their linked accounts.

        :param ctx: The context of the command.
        :param discord_id: The Discord ID of the user to send the message to.
        """
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": f"is using admin_linked for {discord_id}",
        }
        logger.debug(debug)

        links = await config.api.get_discord_links(discord_id)

        if len(links) == 0:
            await ctx.send(
                "You do not have any OSRS accounts linked to this Discord ID. Use the /link command in order to link an account."
            )

        embeds = []
        for i, batch in enumerate(self._batch(links, n=21)):
            embed = discord.Embed(title="Linked Accounts", color=0x00FF00)
            for link in batch:
                link: dict
                if not link:
                    continue
                embed.add_field(
                    name="Account:", value=link.get("name"), inline=True
                )  # inline=False
            embeds.append(embed)

            # max 10 embeds per reply
            if i != 0 and i % 9 == 0:
                await ctx.reply(embeds=embeds)
                embeds = []

        # check if there are any embeds left
        if embeds != []:
            await ctx.reply(embeds=embeds)