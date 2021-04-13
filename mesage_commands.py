import re
import requests as req

VALID_COMMANDS = ['!poke', '!meow', '!warn', 
'!rules', '!website', '!patreon',
'!github', '!invite', '!link',
'!issues', '!list', '!submit',
'!stats', '!kc', '!predict']

# Fun Commands

async def poke_command(message):
    await message.channel.send('Teehee! :3')

async def meow_command(message):
    catResponse = req.get("https://cataas.com/cat?json=true")
    catJSON = catResponse.json()
    catImgURL = "https://cataas.com" + catJSON['url']
    await message.channel.send(catImgURL)

# Informational Commands

async def warn_command(message):
    msg = "```diff" + "\n" \
        + "- **Do not attempt to contact the Jmods or Admins in any channel regarding the status of your Runescape account: Doing so will result in an automatic permanent ban.**" + "\n" \
        + "- **This is your only warning.**" + "\n" \
        + "```\n"
    await message.channel.send(msg)

async def rules_command(message):
    await message.channel.send('<#825137784112807946>')

async def website_command(message):
    await message.channel.send('https://www.osrsbotdetector.com/')

async def patreon_command(message):
    await message.channel.send('https://www.patreon.com/bot_detector')

async def github_command(message, params):
    repo_name = params.split(" ")[0].lower()

    if(repo_name == "core"):
        await message.channel.send('https://github.com/Ferrariic/Bot-Detector-Core-Files') 
    elif(repo_name == "plugin"):
        await message.channel.send('https://github.com/Ferrariic/bot-detector') 
    else:
        await message.channel.send(repo_name + " isn't a valid GitHub repository name. Try 'Core' or 'Plugin'.")

async def invite_command(message):
    await message.channel.send('https://discord.com/invite/JCAGpcjbfP')

async def issues_command(message):
    await message.channel.send('<#822851862016950282>')

async def list_command(message):
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

# Project Stats Commands

async def stats_command(message):
    playersTrackedResponse = req.get("https://www.osrsbotdetector.com/api/site/dashboard/gettotaltrackedplayers")
    otherStatsResponse = req.get("https://www.osrsbotdetector.com/api/site/dashboard/getreportsstats")
    activeInstallsReponse = req.get("https://api.runelite.net/runelite-1.7.4/pluginhub")

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

async def kc_command(message, params):
    playerName = params

    if not is_valid_rsn(playerName):
        await message.channel.send(playerName + " isn't a valid Runescape user name.")
        return

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

async def predict_command(message, params):
    playerName = params

    if not is_valid_rsn(playerName):
        await message.channel.send(playerName + " isn't a valid Runescape user name.")
        return
        
    resp = req.get("https://www.osrsbotdetector.com/api/site/prediction/" + playerName)
    respJSON = resp.json()

    name = respJSON['player_name']
    prediction = respJSON['prediction_label']
    player_id = respJSON['player_id']
    confidence = respJSON['prediction_confidence']
    secondaries = respJSON['secondary_predictions']
          
    msg = "```diff" + "\n" \
        + "+" + " Name: " + str(name) + "\n" \
        + str(plus_minus(prediction,'Real_Player')) + " Prediction: " + str(prediction) + "\n" \
        + str(plus_minus(confidence, 0.75) + " Confidence: " + str(confidence))+ "\n" \
        + "+" + " ID: " + str(player_id) + "\n" \
        + "============\n" \
        + "Prediction Breakdown \n\n"
            
    for predict in secondaries:
        msg += str(plus_minus(predict[0],'Real_Player')) + " " + str(predict[0]) + ": " \
        + str(predict[1])
        msg += "\n" 

    msg += "```\n"
    await message.channel.send(msg)
            
    if message.content.startswith('+ Name') or message.author.id == 825139932817129613:
        message.react('✔️')
        message.react('❌')


# Database Commands

async def submit_command(message, params):
    pass

async def link_command(message, params):
    pass

async def verify_comand(message, params):
    pass

# String Operations
def is_valid_rsn(rsn):
    return re.fullmatch('[\w\d _-]{1,12}', rsn)

# !predict command color changer 
def plus_minus(var, compare):
    diff_control = '-'
    if(isinstance(var, float)):
        if(var > compare):
            diff_control = '+'
    if(isinstance(var, str)):
        if(str(var)==str(compare)):
            diff_control = '+'
    return diff_control