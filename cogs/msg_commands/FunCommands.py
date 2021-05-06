from discord.ext.commands import Cog
from discord.ext.commands import command, check

import discord
import aiohttp
from random import randint
import checks
import help_messages
import subprocess



class FunCommands(Cog, name="Fun Commands"):
    def __init__(self, bot):
        self.bot = bot

    @command(name="poke", description=help_messages.poke_help_msg)
    @check(checks.check_allowed_channel)
    async def poke_command(self, ctx):

        discord_latency = round(self.bot.latency,3)
        ping_api = subprocess.check_call(['ping','-c1','www.osrsbotdetector.com'])
        #bot_api_latency = ping_api

        if ping_api == 0:
            isServerUp = "Online"
        else:
            isServerUp = "Uh-Oh"

        mbed = discord.Embed(color=0x00ff)
        mbed.add_field (name="Teehee", value=f":3", inline=False)
        mbed.add_field (name="Discord Ping:", value=f"{discord_latency} ms", inline=False)
        mbed.add_field (name="BD API Status:", value=f"{isServerUp}", inline=False)
        await ctx.channel.send(embed=mbed)


    @command(name="panic")
    @check(checks.check_allowed_channel)
    async def panic_command(self, ctx):
        await ctx.channel.send("https://i.imgur.com/xAhgsgC.png")


    @command(name="meow", description=help_messages.meow_help_msg)
    @check(checks.check_allowed_channel)
    async def meow_command(self, ctx):
        url = "https://cataas.com/cat/gif?json=true" if randint(0, 1) > 0 else "https://cataas.com/cat?json=true"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    js = await r.json()
                    await ctx.channel.send("https://cataas.com" + js['url'])
                else:
                    await ctx.channel.send("Ouw souwce fo' cats am cuwwentwy down, sowwy :3")


    @command(name="woof", description=help_messages.woof_help_msg)
    @check(checks.check_allowed_channel)
    async def woof_command(self, ctx):
        url = "https://some-random-api.ml/img/dog"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    js = await r.json()
                    await ctx.channel.send(js['link'])
                else:
                    await ctx.channel.send("Who let the dogs out?")


    @command(name="birb", aliases=["bird"], description=help_messages.birb_help_msg)
    @check(checks.check_allowed_channel)
    async def birb_command(self, ctx):
        url = "http://shibe.online/api/birds"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    js = await r.json()
                    await ctx.channel.send(js[0])
                else:
                    await ctx.channel.send("Birds all flew away. :(")


    @command(name="bunny", aliases=["rabbit", "bun"], description=help_messages.bunny_help_msg)
    @check(checks.check_allowed_channel)
    async def bunny_command(self, ctx):
        url = "https://api.bunnies.io/v2/loop/random/?media=gif,png"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    js = await r.json()
                    await ctx.channel.send(js['media']['gif'])
                else:
                    await ctx.channel.send("The buns went on the run.")
                    

def setup(bot):
    bot.add_cog(FunCommands(bot))