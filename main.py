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
        
    if message.content.startswith('!rules') or message.content.startswith('!Rules'):
        await message.channel.send('<#${825137784112807946}>')
        
    if message.content.startswith('!list') or message.content.startswith('!List'):
        await message.channel.send('PENDING - Will be added soon :) Stay Tuned')
        
    if message.content.startswith('!ban') or message.content.startswith('!Ban'):
        msg = "```diff" + "\n" \
                 + "- **Do not attempt to contact the Jmods or Admins in any channel regarding the status of your Runescape account: Doing so will result in an automatic permanent ban.**" + "\n" \
                 + "```\n"
        await message.channel.send(msg)
        
    if message.content.startswith('!website') or message.content.startswith('!Website'):
        await message.channel.send('https://www.osrsbotdetector.com/#/')
        
    if message.content.startswith('!patreon') or message.content.startswith('!Patreon'):
        await message.channel.send('https://www.patreon.com/bot_detector') 
        
    if message.content.startswith('!github core') or message.content.startswith('!github core'):
            await message.channel.send('https://github.com/Ferrariic/Bot-Detector-Core-Files') 
            
    if message.content.startswith('!github plugin') or message.content.startswith('!github plugin'):
            await message.channel.send('https://github.com/Ferrariic/bot-detector') 

    if message.content.startswith('!invite') or message.content.startswith('!Invite'):
        await message.channel.send('https://discord.com/invite/JCAGpcjbfP')

    if message.content.startswith('!issues') or message.content.startswith('!Issues'):
        await message.channel.send('<#${822851862016950282}>')

    if message.content.startswith('!stats') or message.content.startswith('!STATS'):
        playersTrackedResponse = req.get("https://www.osrsbotdetector.com/api/site/dashboard/gettotaltrackedplayers")
        otherStatsResponse = req.get("https://www.osrsbotdetector.com/api/site/dashboard/getreportsstats")
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

        resp = req.get("https://www.osrsbotdetector.com/api/stats/contributions/" + playerName)
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
