import asyncio
import logging
import re
from typing import List

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context
from app.controllers.detective import utils
from repositories.bot_detector_api import BotDetectorAPI as BD_API

logger = logging.getLogger(__name__)

bd_api = BD_API(base_url="", api_key="")


async def submit(ctx: Context, url: str) -> None:
    debug = {
        "author": ctx.author.name,
        "author_id": ctx.author.id,
        "msg": "Send submission",
    }
    logger.debug(debug)

    # max interaction time is 3 sec, with defer it is 15 min
    await ctx.defer()

    # check if url is a pastebin url
    if not url.startswith("https://pastebin.com/"):
        await ctx.reply("Please submit a pastebin url.")
        return

    # get data
    data = await utils._get_pastebin(url)

    if data is None:
        await ctx.reply("could not get pastebin")
        return

    # parse data from pastebin
    user_names = await utils._parse_pastebin(data)

    await ctx.reply(f"Received, {len(user_names)}. Thank you for submitting your list")
    # post parsed data to api (list of strings)
    logger.debug(f"posting, {len(user_names)} to api")
    # asyncio.gather(*[bd_api.create_player(name) for name in user_names])
    logger.debug(f"[DONE] posting, {len(user_names)} to api")
    return
