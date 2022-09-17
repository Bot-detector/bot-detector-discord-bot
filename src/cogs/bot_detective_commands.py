import asyncio
import logging
import re
from typing import List

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context
from src.config import api
from src.utils.checks import DETECTIVE_ROLE, HEAD_DETECTIVE_ROLE, OWNER_ROLE

logger = logging.getLogger(__name__)


class botDetectiveCommands(commands.Cog):
    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot

    async def _parse_pastebin(self, data: str) -> List[str]:
        # get a list of user names from the data
        user_names = [line for line in data.split("\r\n")]
        # validate that the user_names are in line with jagex naming convention
        match = r"^[a-zA-Z0-9_\- ]{1,12}$"
        user_names = [name for name in user_names if re.match(match, name)]
        user_names = list(set(user_names))
        logger.debug(f"parsed names: {len(user_names)}")
        return user_names

    def _batch(self, iterable, n=1) -> list:
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx : min(ndx + n, l)]

    @commands.hybrid_command()
    @commands.has_any_role(
        DETECTIVE_ROLE, HEAD_DETECTIVE_ROLE, OWNER_ROLE
    )
    async def submit(self, ctx: Context, url: str) -> None:
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": "Send submission",
        }
        logger.debug(debug)
        # check if url is a pastebin url
        if not url.startswith("https://pastebin.com/"):
            await ctx.reply("Please submit a pastebin url.")
            return

        # get data from pastebin
        resp: aiohttp.ClientResponse = await self.bot.Session.get(url)

        if not resp.ok:
            await ctx.reply("could not get the pastebin")
            return

        data = await resp.text()
        # parse data from pastebin
        user_names = await self._parse_pastebin(data)

        await asyncio.gather(*[api.create_player(name) for name in user_names])
        # post parsed data to api (list of strings)
        await ctx.reply("Thank you for submitting your list.")
        return

    @commands.hybrid_command()
    @commands.has_any_role(
        DETECTIVE_ROLE, HEAD_DETECTIVE_ROLE, OWNER_ROLE
    )
    async def ban_list(self, ctx: Context, url: str) -> None:
        """ """
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": "Send ban list",
        }
        logger.debug(debug)
        # validate pastebin
        if not url.startswith("https://pastebin.com/"):
            await ctx.reply("Please submit a pastebin url.")
            return

        # get data from pastebin
        resp: aiohttp.ClientResponse = await self.bot.Session.get(url)

        # validate response
        if not resp.ok:
            await ctx.reply("could not get the pastebin")
            return

        # parse data from pastebin
        data = await resp.text()
        user_names = await self._parse_pastebin(data)

        players = await asyncio.gather(
            *[api.get_player(name.replace("_", " ")) for name in user_names]
        )
        logger.debug(f"got players: {len(players)}")

        embeds = []
        i = 0
        for batch in self._batch(players, n=21):
            embed = discord.Embed(title="Ban list", color=discord.Color.red())
            for player in batch:
                player: dict
                if not player:
                    continue
                banned = True if player.get("label_jagex") == 2 else False
                value = f"```{banned}```" if banned else banned
                embed.add_field(name=player.get("name"), value=value, inline=True)
            embed.set_footer(text="True=Banned, False=Not banned")
            embeds.append(embed)

            # max 10 embeds per reply
            if i != 0 and i % 9 == 0:
                await ctx.reply(embeds=embeds)
                embeds = []
            i += 1

        # check if there are any embeds left
        if embeds != []:
            await ctx.reply(embeds=embeds)
        return
