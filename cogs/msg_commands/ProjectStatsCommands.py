from inspect import cleandoc

import aiohttp
import discord
from discord.ext import commands

import checks
import help_messages

class ProjectStatsCommands(commands.Cog, name='Project Stats Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats", description=help_messages.stats_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def stats_command(self, ctx):
        playersTracked = ""
        totalBans = ""
        totalReports = ""
        activeInstalls = ""

        async with self.bot.session.get("https://www.osrsbotdetector.com/api/site/dashboard/gettotaltrackedplayers") as r:
            if r.status == 200:
                js = await r.json()
                playersTracked = js['players'][0]
            else:
                playersTracked = "N/A"

        async with self.bot.session.get("https://www.osrsbotdetector.com/api/site/dashboard/getreportsstats") as r:
            if r.status == 200:
                js = await r.json()
                totalBans = js['bans']
                totalReports = js['total_reports']
            else:
                totalBans = "N/A"
                totalReports = "N/A"

        async with self.bot.session.get("https://api.runelite.net/runelite-1.7.6/pluginhub") as r:
            if r.status == 200:
                js = await r.json()
                activeInstalls = js['bot-detector']
            else:
                activeInstalls = "N/A"


        mbed = await project_stats(playersTracked, totalReports, totalBans, activeInstalls)
        await ctx.send(embed=mbed)


async def project_stats(playersTracked, totalReports, totalBans, activeInstalls):
    mbed = discord.Embed(title=f"Bot Detector Plugin", color=0x00ff00)
    mbed.add_field(name="= Project Stats =", inline=False, value=cleandoc(f"""
            Players Analyzed: {playersTracked:,}"
            Jagex Reports: {totalReports:,}"
            Bans: {totalBans:,}"
            Active Installs: {activeInstalls:,}
        """)
    )

    mbed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117360948-60a24f80-ae87-11eb-8a5a-7ba57f85deb2.png")
    return mbed


def setup(bot):
    bot.add_cog(ProjectStatsCommands(bot))
