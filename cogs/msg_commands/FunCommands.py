import subprocess
from random import randint

import discord
from discord.ext import commands

import help_messages
import utils.roles as roles
from utils import CommonCog, check_allowed_channel


class FunCommands(CommonCog, name="Fun Commands"):
    cog_check = check_allowed_channel

    @commands.command(description=help_messages.poke_help_msg)
    async def poke(self, ctx):
        ping_api = subprocess.check_call(['ping','-c1','www.osrsbotdetector.com'])
        isServerUp = "Online" if not ping_api else "Uh-Oh"

        embed = discord.Embed(color=0x00ff)
        embed.add_field(name="Teehee", value=f":3", inline=False)
        embed.add_field(name="Discord Ping:", value=f"{self.bot.latency:.3f} ms", inline=False)
        embed.add_field(name="BD API Status:", value=f"{isServerUp}", inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    async def panic(self, ctx):
        await ctx.send("https://i.imgur.com/xAhgsgC.png")


    @commands.command(name="meow", description=help_messages.meow_help_msg)
    async def meow(self, ctx):
        url = "https://cataas.com/cat/gif?json=true" if randint(0, 1) > 0 else "https://cataas.com/cat?json=true"

        async with self.bot.session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                await ctx.send("https://cataas.com" + js['url'])
            else:
                await ctx.send("Ouw souwce fo' cats am cuwwentwy down, sowwy :3")


    @commands.command(description=help_messages.woof_help_msg)
    async def woof(self, ctx):
        url = "https://some-random-api.ml/img/dog"

        async with self.bot.session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                await ctx.send(js['link'])
            else:
                await ctx.send("Who let the dogs out?")


    @commands.command(aliases=["bird"], description=help_messages.birb_help_msg)
    async def birb(self, ctx):
        url = "http://shibe.online/api/birds"

        async with self.bot.session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                await ctx.send(js[0])
            else:
                await ctx.send("Birds all flew away. :(")


    @commands.command(aliases=["rabbit", "bun"], description=help_messages.bunny_help_msg)
    async def bunny(self, ctx):
        url = "https://api.bunnies.io/v2/loop/random/?media=gif,png"

        async with self.bot.session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                await ctx.send(js['media']['gif'])
            else:
                await ctx.send("The buns went on the run.")


    @commands.command( description=help_messages.event_help_msg)
    async def event(self, ctx, *, toggle_option):
        member = ctx.author
        event_role = discord.utils.find(roles.special_roles["An Eventful Chum"]["role_id"])

        if toggle_option.lower() == "on":
            member = ctx.author
            await member.add_roles(event_role)
        elif toggle_option.lower() == "off":
            await member.remove_roles(event_role)
        else:
            await ctx.reply("Use `!event on` or `!event off`.")


def setup(bot):
    bot.add_cog(FunCommands(bot))
