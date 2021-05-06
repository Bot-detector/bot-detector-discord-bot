from discord.ext.commands import Cog
from discord.ext.commands import command

import discord

class ModCommands(Cog, name='Moderator Commands'):

    def __init__(self, bot):
        self.bot = bot

    @command(name="warn", aliases=["youvedoneitnow"], hidden=True)
    async def warn_command(self, ctx):
        mbed = await warn_msg()
        await ctx.channel.send(embed=mbed)

async def warn_msg():
    mbed = discord.Embed(title=f"WARNING", color=0xff0000)
    mbed.add_field (name="= WARNING MESSAGE =", value="**Do not attempt to contact the Jmods or Admins in any channel regarding the status of your Runescape account: Doing so will result in an automatic permanent ban.**" + "\n" \
            + "**This is your only warning.**" + "\n", inline=False)
    mbed.set_image(url="https://user-images.githubusercontent.com/5789682/117366156-59327480-ae8e-11eb-8b08-6cf815d8a36e.png")
    return mbed

def setup(bot):
    bot.add_cog(ModCommands(bot))



