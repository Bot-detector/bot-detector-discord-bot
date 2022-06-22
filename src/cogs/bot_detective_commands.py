import asyncio
import json
from typing import List
import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context
from src.config import api
import re
import logging
from inspect import cleandoc

logger = logging.getLogger(__name__)

class botDetectiveCommands(commands.Cog):
    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot

    async def _parse_pastebin(self, data:str) -> List[str]:
        # get a list of user names from the data
        user_names = [line for line in data.split("\r\n")]
        # validate that the user_names are in line with jagex naming convention
        match = r"^[a-zA-Z0-9_\- ]{1,12}$"
        user_names = [name for name in user_names if re.match(match, name)]
        return user_names

    # TODO: help message
    @commands.command()
    async def submit(self, ctx: Context, url: str, label: str = None) -> None:
        logger.debug("received submission")
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

        await asyncio.gather(
            *[api.create_player(name) for name in user_names]
        )
        # post parsed data to api (list of strings)
        await ctx.reply("Thank you for submitting your list.")
        return

    @commands.command()
    async def ban_list(self, ctx: Context, url) -> None:
        """ """
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
            *[api.get_player(name.replace("_"," ")) for name in user_names]
        )

        output = []
        for player in players:
            if player is None:
                continue
            banned = True if player.get("label_jagex") == 2 else False
            output.append({"player": player.get("name"), "banned":banned})

        output = cleandoc(f"""
            ```js
            {output}
            ```
            """
        )
        await ctx.reply(output)
        return
