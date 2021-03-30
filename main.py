import discord
import os
from dotenv import load_dotenv
import requests as req

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "a round of wintertodt is about to begin" in message.content.lower():
        await message.channel.send('Chop chop!')

    if message.content.startswith('!stats') or message.content.startswith('!STATS'):
        playersTrackedResponse = req.get("http://osrsbot-detector.ddns.net:5000/site/dashboard/gettotaltrackedplayers")
        otherStatsResponse = req.get("http://osrsbot-detector.ddns.net:5000/site/dashboard/getreportsstats")
        activeInstallsReponse = req.get("https://api.runelite.net/runelite-1.7.3.1/pluginhub")
        
        playersJSON = playersTrackedResponse.json()
        otherStatsJSON= otherStatsResponse.json()
        activeInstallsJSON = activeInstallsReponse.json()

        playersTracked = playersJSON['players'][0]
        totalBans = otherStatsJSON['bans']
        totalReports = otherStatsJSON['total_reports']
        activeInstalls = activeInstallsJSON['bot-detector']
        
        msg = "```Project Stats:\n" \
                + "Players Analyzed: " + str(playersTracked) + "\n"\
                + "Reports Sent to Jagex: " + str(totalReports) + "\n"\
                + "Resultant Bans: " + str(totalBans) + "\n"\
                + "Active Installs: " + str(activeInstalls) \
                + "```"

        await message.channel.send(msg)

    if message.content.startswith('!kc') or message.content.startswith('!KC'):
        playerName = message.content[4:16]

        resp = req.get("http://osrsbot-detector.ddns.net:5000/stats/contributions/" + playerName)
        respJSON = resp.json()

        reports = respJSON['reports']
        bans = respJSON['bans']
        possible_bans = respJSON['possible_bans']


        msg = "```" + playerName + "'s Stats: \n" \
                 + "Reports Submitted: " + str(reports) + "\n" \
                 + "Probable/Pending Bans: " + str(possible_bans) + "\n" \
                 + "Confirmed Bans: " + str(bans) + "```\n"

        await message.channel.send(msg)
            









@client.event
async def on_member_join(member):
    pass

client.run(os.getenv('TOKEN'))
