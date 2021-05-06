from discord.ext.commands import Cog
from discord.ext.commands import command, check

import aiohttp
import checks
import help_messages
import discord

class ProjectStatsCommands(Cog, name='Project Stats Commands'):

    def __init__(self, bot):
        self.bot = bot

    @command(name="stats", description=help_messages.stats_help_msg)
    @check(checks.check_allowed_channel)
    async def stats_command(self, ctx):

        async with aiohttp.ClientSession() as session:
            playersTracked = ""
            totalBans = ""
            totalReports = ""
            activeInstalls = ""

            async with session.get("https://www.osrsbotdetector.com/api/site/dashboard/gettotaltrackedplayers") as r:
                if r.status == 200:
                    js = await r.json()
                    playersTracked = js['players'][0]
                else:
                    playersTracked = "N/A"

            async with session.get("https://www.osrsbotdetector.com/api/site/dashboard/getreportsstats") as r:
                if r.status == 200:
                    js = await r.json()
                    totalBans = js['bans']
                    totalReports = js['total_reports']
                else:
                    totalBans = "N/A"
                    totalReports = "N/A"

            async with session.get("https://api.runelite.net/runelite-1.7.6/pluginhub") as r:
                if r.status == 200:
                    js = await r.json()
                    activeInstalls = js['bot-detector']
                else:
                    activeInstalls = "N/A" 


        mbed = await project_stats(playersTracked, totalReports, totalBans, activeInstalls)

        await ctx.channel.send(embed=mbed)

async def project_stats(playersTracked, totalReports, totalBans, activeInstalls):
    mbed = discord.Embed(title=f"Bot Detector Plugin", color=0x00ff00)
    mbed.add_field (name="= Project Stats =", value=f"Players Analyzed: {playersTracked:,}" + "\n" \
        + f"Jagex Reports: {totalReports:,}" + "\n" \
        + f"Bans: {totalBans:,}" + "\n" \
        + f"Active Installs: {activeInstalls:,}", inline=False)
    return mbed

def setup(bot):
    bot.add_cog(ProjectStatsCommands(bot))
