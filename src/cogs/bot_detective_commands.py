import discord
from discord.ext import commands
from discord.ext.commands import Context


import re
import requests


class botDetectiveCommands(commands.Cog):
    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot

    # TODO: help message
    @commands.command()
    async def submit(self, ctx: Context, url: str, label: str = None) -> None:
        # check if url is a pastebin url
        if not url.startswith("https://pastebin.com/"):
            await ctx.reply("Please submit a pastebin url.")
            return
        # get data from pastebin
        data = requests.get(url).text
        # get a list of user names from the data
        user_names = [line for line in data.split("\n")]
        # validate that the user_names are in line with jagex naming convention
        match = r"^[a-zA-Z0-9_]{1,12}$"
        user_names = [name for name in user_names if re.match(match, name)]
        # parse data from pastebin => list of user names (list of strings)
        # post parsed data to api (list of strings)
        await ctx.reply("Thank you for submitting your list.")
        return

    @commands.command()
    async def ban_list(self, ctx: Context, url) -> None:
        """ """
        # get data from pastebin
        # parse data from pastebin => list of user names
        # get account status for the user names
        # return data
        return
