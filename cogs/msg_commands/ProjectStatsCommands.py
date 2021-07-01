from inspect import cleandoc

import discord
from discord.ext import commands

import help_messages
from utils import CommonCog, checks


class ProjectStatsCommands(CommonCog, name='Project Stats Commands'):
    cog_check = checks.check_allowed_channel

    @commands.command(description=help_messages.stats_help_msg)
    async def stats(self, ctx):
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

        async with self.bot.session.get("https://api.runelite.net/runelite-1.7.14/pluginhub") as r:
            if r.status == 200:
                js = await r.json()
                activeInstalls = js['bot-detector']
            else:
                activeInstalls = "N/A"


        embed = await project_stats(playersTracked, totalReports, totalBans, activeInstalls)
        await ctx.send(embed=embed)


async def project_stats(playersTracked, totalReports, totalBans, activeInstalls):
    embed = discord.Embed(title="Bot Detector Plugin", color=0x00ff00)
    embed.add_field(name="= Project Stats =", inline=False, value=cleandoc(f"""
            Players Analyzed: {playersTracked:,}
            Confirmed Players: {(totalReports-totalBans):,}
            Confirmed Bans: {totalBans:,}
            Active Installs: {activeInstalls:,}
        """)
    )

    embed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117360948-60a24f80-ae87-11eb-8a5a-7ba57f85deb2.png")
    return embed


def setup(bot):
    bot.add_cog(ProjectStatsCommands(bot))
