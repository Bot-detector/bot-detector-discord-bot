from discord.ext.commands import Cog
from discord.ext.commands import command

class ModCommands(Cog, name='Moderator Commands'):

    def __init__(self, bot):
        self.bot = bot

    @command(name="warn", aliases=["youvedoneitnow"], hidden=True)
    async def warn_command(self, ctx):
        msg = "```diff" + "\n" \
            + "- **Do not attempt to contact the Jmods or Admins in any channel regarding the status of your Runescape account: Doing so will result in an automatic permanent ban.**" + "\n" \
            + "- **This is your only warning.**" + "\n" \
            + "```\n"
        await ctx.channel.send(msg)

def setup(bot):
    bot.add_cog(ModCommands(bot))



