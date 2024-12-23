import logging
import random
import subprocess

import discord
from discord.ext import commands
from discord.ext.commands import Context, Cog

logger = logging.getLogger(__name__)


class funCommands(Cog):
    def __init__(self, bot: discord.Client) -> None:
        """
        Initialize the funCommands class.
        :param bot: The discord bot client.
        """
        self.bot = bot

    async def __web_request(self, url: str) -> dict:
        """
        Make a web request to the specified url.

        :param url: The url to make the request to.
        :return: The response from the request.
        """
        async with self.bot.Session.get(url) as response:
            if response.status != 200:
                logger.error({"status": response.status, "url": url})
                return None
            return await response.json()

    @commands.hybrid_command(name="poke")
    async def poke(self, ctx: Context):
        """
        Ping the bot and the botDetective API.
        """
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": "requested a poke",
        }
        logger.debug(debug)
        url = "https://api.prd.osrsbotdetector.com"
        ping = await self.__web_request(url)
        isServerUp = "Online" if ping is not None else "Uh-Oh"

        embed = discord.Embed(color=0x00FF)
        embed.add_field(name="Teehee", value=f":3", inline=False)
        embed.add_field(
            name="Discord Ping:", value=f"{self.bot.latency:.3f} ms", inline=False
        )
        embed.add_field(name="BD API Status:", value=f"{isServerUp}", inline=False)
        await ctx.reply(embed=embed)
        pass

    @commands.hybrid_command()
    async def panic(self, ctx: Context):
        """
        Send a panic image.
        """
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": "requested a panic",
        }
        logger.debug(debug)
        await ctx.send("https://i.imgur.com/xAhgsgC.png")

    @commands.hybrid_command(name="meow")
    async def meow(self, ctx: Context):
        """
        Send a random cat image.
        """
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": "requested a cat",
        }
        logger.debug(debug)
        if random.randint(0, 1) > 0:
            url = "https://cataas.com/cat/gif?json=true"
        else:
            url = "https://cataas.com/cat?json=true"

        data = await self.__web_request(url)
        if data is None:
            await ctx.reply("Ouw souwce fo' cats am cuwwentwy down, sowwy :3")
        else:
            await ctx.reply("https://cataas.com" + data["url"])
        return

    @commands.hybrid_command()
    async def woof(self, ctx: Context):
        """
        Send a random dog image.
        """
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": "requested a dog",
        }
        logger.debug(debug)
        url = "https://some-random-api.ml/img/dog"

        data = await self.__web_request(url)
        if data is None:
            await ctx.reply("Who let the dogs out?")
        else:
            await ctx.reply(data.get("link"))
        return

    @commands.hybrid_command(aliases=["bird"])
    async def birb(self, ctx: Context):
        """
        Send a random bird image.
        """
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": "requested a bird",
        }
        logger.debug(debug)
        url = "http://shibe.online/api/birds"

        data = await self.__web_request(url)
        if data is None:
            await ctx.reply("Birds all flew away. :(")
        else:
            await ctx.reply(data[0])
        return

    @commands.hybrid_command(aliases=["rabbit", "bun"])
    async def bunny(self, ctx: Context):
        """
        Send a random bunny image.
        """
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": "requested a bunny",
        }
        logger.debug(debug)
        url = "https://api.bunnies.io/v2/loop/random/?media=gif,png"

        data = await self.__web_request(url)
        if data is None:
            await ctx.reply("The buns went on the run.")
        else:
            await ctx.reply(data["media"]["gif"])
        return
