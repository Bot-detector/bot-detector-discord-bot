import subprocess
from random import randint

import aiohttp
import discord
from discord.ext import commands

import checks
import help_messages


class FunCommands(commands.Cog, name="Fun Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poke", description=help_messages.poke_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def poke_command(self, ctx):
        ping_api = subprocess.check_call(['ping','-c1','www.osrsbotdetector.com'])
        isServerUp = "Online" if not ping_api else "Uh-Oh"

        embed = discord.Embed(color=0x00ff)
        embed.add_field(name="Teehee", value=f":3", inline=False)
        embed.add_field(name="Discord Ping:", value=f"{self.bot.latency:.3f} ms", inline=False)
        embed.add_field(name="BD API Status:", value=f"{isServerUp}", inline=False)
        await ctx.send(embed=embed)


    @commands.command(name="panic")
    @commands.check(checks.check_allowed_channel)
    async def panic_command(self, ctx):
        await ctx.send("https://i.imgur.com/xAhgsgC.png")


    @commands.command(name="meow", description=help_messages.meow_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def meow_command(self, ctx):
        url = "https://cataas.com/cat/gif?json=true" if randint(0, 1) > 0 else "https://cataas.com/cat?json=true"

        async with self.bot.session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                await ctx.send("https://cataas.com" + js['url'])
            else:
                await ctx.send("Ouw souwce fo' cats am cuwwentwy down, sowwy :3")


    @commands.command(name="woof", description=help_messages.woof_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def woof_command(self, ctx):
        url = "https://some-random-api.ml/img/dog"

        async with self.bot.session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                await ctx.send(js['link'])
            else:
                await ctx.send("Who let the dogs out?")


    @commands.command(name="birb", aliases=["bird"], description=help_messages.birb_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def birb_command(self, ctx):
        url = "http://shibe.online/api/birds"

        async with self.bot.session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                await ctx.send(js[0])
            else:
                await ctx.send("Birds all flew away. :(")


    @commands.command(name="bunny", aliases=["rabbit", "bun"], description=help_messages.bunny_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def bunny_command(self, ctx):
        url = "https://api.bunnies.io/v2/loop/random/?media=gif,png"

        async with self.bot.session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                await ctx.send(js['media']['gif'])
            else:
                await ctx.send("The buns went on the run.")


def setup(bot):
    bot.add_cog(FunCommands(bot))
