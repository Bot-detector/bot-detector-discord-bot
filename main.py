import discord
import os
from dotenv import load_dotenv
import re
import requests as req
from bs4 import BeautifulSoup

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    # easter eggs
        
    if "a round of wintertodt is about to begin" in message.content.lower():
        await message.channel.send('Chop chop!')

    
    if message.content.startswith('!meow') or message.content.startswith('!Meow'):
        catResponse = req.get("https://cataas.com/cat?json=true")
        catJSON = catResponse.json()
        catImgURL = "https://cataas.com/" + catJSON['url']
        await message.channel.send(catImgURL)

        
     # channel links
        
    if message.content.startswith('!rules') or message.content.startswith('!Rules'):
        await message.channel.send('<#825137784112807946>')
        
    if message.content.startswith('!issues') or message.content.startswith('!Issues'):
        await message.channel.send('<#822851862016950282>')
        
   # list dm process
        
    if message.content.startswith('!list') or message.content.startswith('!List'):
        msg = "Please send a link to a Pastebin URL containing your name list." + "\n" \
        + "Example: !submit https://pastebin.com/iw8MmUzg" + "\n" \
        + "___________" + "\n" \
        + "Acceptable Formatting:" + "\n" \
        + "Player 1" + "\n" \
        + "Player 2" + "\n" \
        + "Player 3" + "\n" \
        + "Player 4" + "\n" \
        + "Player 5" + "\n" \
        + "___________" + "\n" \
        + "Pastebin Settings:" + "\n" \
        + "Syntax Highlighting: None" + "\n" \
        + "Paste Expiration: 1 Day" + "\n" \
        + "Paste Exposure: Public" + "\n" \
        + "Folder: No Folder Selected" + "\n" \
        + "Password: {leave blank - no password needed}" + "\n" \
        + "Paste Name / Title: {Include your Label Here}" + "\n" 
        await message.author.send(msg)
        
    if message.content.startswith('!submit') or message.content.startswith('!Submit'):
        newlines = list()
        paste_url = message.content[8:100]
  
        data = req.get(paste_url)
        soup = BeautifulSoup(data.content, 'html.parser')
        output = soup.findAll('textarea')
        lines = str(output[0]).strip('<textarea class="textarea">').strip('<"/"').replace('\r','').splitlines()
        
        for line in lines:
            L = re.fullmatch('[\w\d _-]{0,12}', line)
            if L:
                if line != '':
                    newlines.append(line)
        
        outputLabel = soup.findAll('title')
        label = str(outputLabel[0]).replace('<title>',"").replace(' - Pastebin.com</title>','')
        
        msg = "Paste Information" + "\n" \
        + "_____________________" + "\n" \
        + "Number of Names: " + str(len(newlines)) + "\n" \
        + "Label: " + str(label) + "\n" \
        + "Samples: " + str(newlines[0:10]) + "\n"
        
        await message.channel.send(msg)
    
    # admin commands
        
    if message.content.startswith('!ban') or message.content.startswith('!Ban'):
        msg = "```diff" + "\n" \
                 + "- **Do not attempt to contact the Jmods or Admins in any channel regarding the status of your Runescape account: Doing so will result in an automatic permanent ban.**" + "\n" \
                 + "```\n"
        await message.channel.send(msg)
        
    # links
        
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
        
    # plugin and database stats

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
        
    # player stats

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
