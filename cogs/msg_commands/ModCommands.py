import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils import CommonCog

load_dotenv()
token = os.getenv("API_AUTH_TOKEN")

class ModCommands(CommonCog, name="Moderator Commands"):

    @commands.has_permissions(kick_members=True)
    @commands.command(aliases=["youvedoneitnow"])
    async def jmod(self, ctx):
        embed = await jmod_warn_msg()
        await ctx.send(embed=embed)


    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, limit):
        channel = ctx.guild.get_channel(ctx.channel.id)
        await channel.purge(limit = int(limit))


async def jmod_warn_msg():
    embed = discord.Embed(title="WARNING", color=0xff0000)
    embed.add_field (name="= WARNING MESSAGE =", value="**Do not attempt to contact the Jmods or Admins in any channel regarding the status of your Runescape account: Doing so will result in an automatic permanent ban.**" + "\n" \
            + "**This is your only warning.**" + "\n", inline=False)
    embed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117366156-59327480-ae8e-11eb-8b08-6cf815d8a36e.png")
    return embed


def setup(bot):
    bot.add_cog(ModCommands(bot))
