# /app/controllers/fun/ping.py
import aiohttp
import asyncio
from time import time
from discord.ext.commands import Context
import logging
import discord

logger = logging.getLogger(__name__)


async def measure_latency(url="https://www.osrsbotdetector.com/api/", timeout=5):
    async with aiohttp.ClientSession() as session:
        start_time = time()
        try:
            async with session.get(url, timeout=timeout) as response:
                _latency = time() - start_time
                logger.info({"latency": _latency})
                return _latency
        except asyncio.TimeoutError:
            logger.error({"latency": timeout, "type": "timeout"})
            return None


async def ping(ctx: Context):
    _latency = await measure_latency()
    _status = "Offline" if _latency is None else "Online"

    embed = discord.Embed(color=0x00FF)
    embed.add_field(name="Teehee", value=f":3", inline=False)
    embed.add_field(name="API Ping:", value=f"{_latency:.3f} ms", inline=False)
    embed.add_field(name="API Status:", value=f"{_status}", inline=False)
    await ctx.reply(embed=embed)
