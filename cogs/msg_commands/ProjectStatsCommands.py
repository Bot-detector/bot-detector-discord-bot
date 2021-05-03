from discord.ext.commands import Cog
from discord.ext.commands import command, check

import aiohttp
import checks

class ProjectStatsCommands(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="stats")
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

        msg = "```Project Stats:\n" \
            + "Players Analyzed: " + str(playersTracked) + "\n" \
            + "Reports Sent to Jagex: " + str(totalReports) + "\n" \
            + "Resultant Bans: " + str(totalBans) + "\n" \
            + "Active Installs: " + str(activeInstalls) \
            + "```"

        await ctx.channel.send(msg)

def setup(bot):
    bot.add_cog(ProjectStatsCommands(bot))
