import os
import re
import json
import string
import discord
import random
import pandas as pd
from random import randint
from datetime import datetime, timezone
import requests as req

import sql
import patron

VALID_COMMANDS = ['!poke', '!meow', '!warn', 
'!rules', '!website', '!patreon',
'!github', '!invite', '!link',
'!issues', '!list', '!submit',
'!stats', '!kc', '!predict', '!verify',
'!primary','!heatmap', '!utc',
'!woof', '!region', '!map']

# Fun Commands

async def poke_command(message):
    await message.channel.send('Teehee! :3')

async def meow_command(message):

    if(randint(0,1) == 1):
        url = "https://cataas.com/cat/gif?json=true"
    else:
        url = "https://cataas.com/cat?json=true"

    catResponse = req.get(url)
    catJSON = catResponse.json()
    catImgURL = "https://cataas.com" + catJSON['url']
    await message.channel.send(catImgURL)

async def woof_command(message):
    url = "https://some-random-api.ml/img/dog"

    dogResponse = req.get(url)
    dogJSON = dogResponse.json()
    dogImgURL = dogJSON['link']
    await message.channel.send(dogImgURL)


async def utc_time_command(message):
    await message.channel.send(datetime.now(timezone.utc))

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
    activeInstallsReponse = req.get("https://api.runelite.net/runelite-1.7.5/pluginhub")

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

    msg += "Click the reactions below to give feedback on the above prediction:"
    my_msg = await message.channel.send(msg)
            
    await my_msg.add_reaction('✔️')
    await my_msg.add_reaction('❌')

# Heatmap and Region Commands

async def region_command(message, params):
    regionName = params
    data = patron.getHeatmapRegion(regionName)
    removedDuplicates, regionIDs, region_name = patron.displayDuplicates(data)
    if len(removedDuplicates)<30:    
        if len(removedDuplicates)<2:
            regionTrueName = patron.Autofill(removedDuplicates, regionName)
            regionSelections = patron.allHeatmapSubRegions(regionTrueName, region_name, regionIDs, removedDuplicates)
            msg = "```diff" + "\n" \
            + "+ Input: " + str(regionName) + "\n" \
            + "+ Selection From: " + str(', '.join([str(elem) for elem in removedDuplicates])) + "\n" \
            + "+ Selected: " + str(regionTrueName) + "\n" \
            + "+ Region Selections: " + str(', '.join([str(elem) for elem in regionSelections])) + "\n" \
            + "```"
        else:
            regionTrueName = patron.Autofill(removedDuplicates, regionName)
            regionSelections = patron.allHeatmapSubRegions(regionTrueName, region_name, regionIDs, removedDuplicates)
            msg = "```diff" + "\n" \
            + "+ Input: " + str(regionName) + "\n" \
            + "+ Selection From: " + str(', '.join([str(elem) for elem in removedDuplicates])) + "\n" \
            + "+ Selected: " + str(regionTrueName) + "\n" \
            + "+ Region Selections: " + str(', '.join([str(elem) for elem in regionSelections])) + "\n" \
            + "```"
    else:
        msg = "```diff" + "\n" \
        + "- More than 30 Regions selected. Please refine your search." + "\n" \
        + "```"
    await message.channel.send(msg)

# Patron Heatmap command

async def heatmap_command(message, params):
    regionName = params
    sql = ('''
    SELECT DISTINCT
        rpts2.*,
        rpts.x_coord,
        rpts.y_coord,
        rpts.region_id
    FROM Reports rpts
        INNER JOIN (
            SELECT 
                max(rp.id) id,
                pl.name,
                pl.confirmed_player,
                pl.confirmed_ban
            FROM Players pl
            inner join Reports rp on (pl.id = rp.reportedID)
            WHERE 1
                and (pl.confirmed_ban = 1 or pl.confirmed_player = 1)
                and rp.region_id = %s
            GROUP BY
                pl.name,
                pl.confirmed_player,
                pl.confirmed_ban
        ) rpts2
    ON (rpts.id = rpts2.id)
    ''')
    
    data = patron.getHeatmapRegion(regionName)
    print(data)
    removedDuplicates, regionIDs, region_name = patron.displayDuplicates(data)
    print(removedDuplicates)
    print(regionIDs)
    print(region_name)
    
    if len(removedDuplicates)<30:    
        regionTrueName = patron.Autofill(removedDuplicates, regionName)
        regionSelections = patron.allHeatmapSubRegions(regionTrueName, region_name, regionIDs, removedDuplicates)
        regionid = regionSelections[0]
        try:
            await runAnalysis(regionSelections, regionTrueName, sql)
        except IndexError as i:
            print(e)
            await message.channel.send(f'Not enough data for {params}, sorry!')
        except Exception as e:
            print(e) 
            msg = "Image could not be rendered due to Low Data Pool size, or another error. Please select a new Region."
    else:
        msg = ">30 Regions selected. Please refine your search."
        

    await message.channel.send(file=discord.File(f'{os.getcwd()}/{regionid}.png'))
    
    patron.CleanupImages(regionSelections)
    

async def map_command(message, params):
    regionName = params
    data = sql.getHeatmapRegion(regionName)
    removedDuplicates, regionIDs, region_name = sql.displayDuplicates(data)
    if len(removedDuplicates)<10:    
        regionTrueName = sql.Autofill(removedDuplicates, regionName)
        regionSelections = sql.allHeatmapSubRegions(regionTrueName, region_name, regionIDs, removedDuplicates)
        msg = str('https://raw.githubusercontent.com/Ferrariic/OSRS-Visible-Region-Images/main/Region_Maps/{}.png'.format(regionSelections[0]))
    else:
        msg = "```diff" + "\n" \
        + "- More than 10 Regions selected. Please refine your search." + "\n" \
        + "```"
    await message.channel.send(msg)
    
# Database Commands

async def submit_command(message, params, recipient):
    errors = "No Errors"
    paste_url = params

    sqlLabelInsert = ('''
        INSERT IGNORE `labels_submitted`(`Label`) VALUES (%s)
    ''')

    sqlPlayersInsert = ('''
        INSERT IGNORE `players_submitted`(`Players`) VALUES (%s)
    ''')

    sqlLabelID = ('''
        SELECT ID FROM `labels_submitted` WHERE Label = %s
    ''')

    sqlPlayerID = ('''
        SELECT ID FROM `players_submitted` WHERE Players = %s
    ''')

    sqlInsertPlayerLabel = ('''
        INSERT IGNORE `playerlabels_submitted`(`Player_ID`, `Label_ID`) VALUES (%s, %s)
    ''')
    
    paste_soup = sql.get_paste_data(paste_url)
    List = sql.get_paste_names(paste_soup)
    labelCheck = sql.get_paste_label(paste_soup)

    try:
        sql.execute_sql(sqlLabelInsert, insert=True, param=[labelCheck])
        
    except Exception as e: #common exception is duplicate label entry, will be pulled later down the line
        errors = e
        pass

    try:
        sql.InsertPlayers(sqlPlayersInsert, List)
    except Exception as e: #common exception is duplicate player entry, will be pulled later down the line
        errors = e
        pass

    try: 
        dfLabelID = pd.DataFrame(sql.execute_sql(sqlLabelID, insert=False, param=[labelCheck]))
        playerID = sql.PlayerID(sqlPlayerID, List)
        sql.InsertPlayerLabel(sqlInsertPlayerLabel, playerID, dfLabelID)
    except Exception as e: #attempts to insert the player IDs and player labels if pulled, will not pull if these values do not exist.
        errors = e
        pass
    
    msg = "```diff" + "\n" \
        + "Paste Information Submitted" + "\n" \
        + "_____________________" + "\n" \
        + "+ Link: " + str(paste_url) + "\n" \
        + "+ Errors: " + str(errors) + "\n" \
        + "```"

    await recipient.send(msg)

async def primary_command(message, params):
    playerName = params
    discord_id = message.author.id

    if not is_valid_rsn(playerName):
        await message.channel.send(playerName + " isn't a valid Runescape user name.")
        return

    msgDoesNotExist = "```diff" + "\n" \
            + "- Player does not exist. Please verify that you have typed in the username correctly." + "\n" \
            + "```"
    msgNotConnected = "```diff" + "\n" \
            + "- You are not connected to this player. You must verify your link to this player with !link <RSN>." + "\n" \
            + "```"
    msgPendingVerification = "```diff" + "\n" \
            + "- You are pending verification on this player. Please verify this account with !link <RSN>" + "\n" \
            + "```"
    msgPlayerUnverified = "```diff" + "\n" \
            + "- The account you are attempting to link is Unverified. Please !link <RSN> and verify this account." + "\n" \
            + "```"
    msgNULLError = "```diff" + "\n" \
            + "- Primary values could not be reset to NULL. Please contact an Administrator." + "\n" \
            + "```"
    msgPrimarySetError = "```diff" + "\n" \
        + "- Your player could not be assigned a Primary value. Please contact an Administrator." + "\n" \
        + "```"
    msgConfirmedPrimary = "```diff" + "\n" \
        + "+ Player has been successfully updated as Primary." + "\n" \
        + "```"

    player_id, exists = sql.verificationPull(playerName)
    if exists:
        check, verified = sql.discord_verification_check(discord_id, player_id)
        if check:
            if verified:
                data, verified_account = sql.VerifyRSNs(discord_id, player_id)
                if verified_account:
                    PrimaryNULL = sql.insertPrimaryNULL(discord_id)
                    if PrimaryNULL:
                        PrimaryTRUE = sql.insertPrimaryTRUE(discord_id, player_id)
                        if PrimaryTRUE:
                            print("Player has been successfully updated as Primary.")
                            msg = msgConfirmedPrimary
                        else:
                            print("Your player could not be assigned a Primary value. Please contact an Administrator.")
                            msg = msgPrimarySetError
                    else:
                        print("Primary values could not be reset to NULL. Please contact an Administrator.")
                        msg = msgNULLError
                else:
                    print("The account you are attempting to link is Unverified. Please !link <RSN> and verify this account.")
                    msg = msgPlayerUnverified
            else:
                print("You are pending verification on this player. Please verify this account with !link <RSN>")
                msg = msgPendingVerification
        else:
            print("You are not connected to this player. You must verify your link to this player with !link <RSN>.")
            msg = msgNotConnected
    else:
        print("Player does not exist. Please verify that you have typed in the username correctly.")
        msg = msgDoesNotExist

    await message.author.send(msg)
    
async def link_command(message, params):
    playerName = params

    if not is_valid_rsn(playerName):
        await message.channel.send(playerName + " isn't a valid Runescape user name.")
        return

    owner_id = 0
    code = id_generator()
    discord_id = message.author.id

    msgPassed = "```diff" + "\n" \
            + "====== STATUS ======\n" \
            + "Request to link RSN: " + str(playerName) + "\n" \
            + "Your discord ID is: " + str(discord_id) + "\n" \
            + "Access Code: " + str(code) + "\n" \
            + "====== SETUP ======\n" \
            + "+ Please read through these instructions." + "\n" \
            + "+ 1. Open Old School Runescape through RuneLite." + "\n" \
            + "+ 2. Login as: '" + str(playerName) + "'." + "\n" \
            + "+ 3. Join the clan channel: 'Ferrariic'." + "\n" \
            + "+ 4. Verify that a Plugin Admin or Plugin Moderator is present in the channel." + "\n" \
            + "+ 5. Type into the Clan Chat: '!Code:" + str(code) + "'." + "\n" \
            + "+ 6. Check your Discord DMs for a 'Verification' message." + "\n" \
            + "+ 7. Verification Process Complete." + "\n" \
            + "====== INFO ======\n" \
            + "+ You may link multiple Runescape accounts via this method." + "\n" \
            + "+ If you change the name of your account(s) you must repeat this process with your new RSN(s)." + "\n" \
            + "+ In the event of a name change please allow some time for your data to be transferred over." + "\n" \
            + "====== NOTICE ======\n" \
            + "- Do not delete this message." + "\n" \
            + "- If this RSN was submitted in error, please type '!link <Your Correct RSN>'." + "\n" \
            + "- This code will not expire, it is tied to your unique RSN:Discord Pair." + "\n" \
            + "- If you are unable to become 'Verified' through this process, please contact an administrator for assistance." + "\n" \
            + "```"

    msgInUse = "```diff" + "\n" \
            + "- RSN is currently in use. Please contact an Administrator." + "\n" \
            + "```"

    msgInstallPlugin = "```diff" + "\n" \
            + "- This user has not installed the Bot Detector plugin, or this user does not exist." + "\n" \
            + "- Please install the plugin or re-enter your !link <RSN> command." + "\n" \
            + "```"

    msgVerified = "```diff" + "\n" \
            + "+ Player: " + str(playerName) + "\n" \
            + "====== Verification Information ======\n" \
            + "+ Player is: Verified." + "\n" \
            + "```"

    msgUnverified = "```diff" + "\n" \
            + "+ Player: " + str(playerName) + "\n" \
            + "====== Verification Information ======\n" \
            + "- Player is: Unverified." + "\n" \
            + "```"

    player_id, exists = sql.verificationPull(playerName)
    if exists:
        check, verified, owner_list = sql.verification_check(player_id)
        if verified:
            msg = msgVerified
        else:
            if check:
                if int(discord_id) not in owner_list:
                    sql.verificationInsert(discord_id, player_id, code)
                    msg = msgPassed
                else:
                    msg = msgInUse
            else:
                sql.verificationInsert(discord_id, player_id, code)
                msg = msgPassed
    else:
        msg = msgInstallPlugin

    await message.author.send(msg)

async def verify_comand(message, params):
    playerName = params

    if not is_valid_rsn(playerName):
        await message.channel.send(playerName + " isn't a valid Runescape user name.")
        return

    owner_id = 0
            
    msgVerified = "```diff" + "\n" \
            + "+ Player: " + str(playerName) + "\n" \
            + "====== Verification Information ======\n" \
            + "+ Player is: Verified." + "\n" \
            + "```"

    msgUnverified = "```diff" + "\n" \
            + "+ Player: " + str(playerName) + "\n" \
            + "====== Verification Information ======\n" \
            + "- Player is: Unverified." + "\n" \
            + "```"
            
    player_id, exists = sql.verificationPull(playerName)
    if exists:
        check, verified, owner_list = sql.verification_check(player_id)
        if verified:
            msg = msgVerified
        else:
            msg = msgUnverified
    else:
        msg = msgUnverified
            
    await message.channel.send(msg)

# String Operations
def is_valid_rsn(rsn):
    return re.fullmatch('[\w\d _-]{1,12}', rsn)

# ID Generator command

def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


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

# Analysis run for Patron Heatmap
async def runAnalysis(regionSelections, regionTrueName, sql):
    region_id = regionSelections[0]
    data = patron.execute_sql(sql, param=[region_id])
    df = pd.DataFrame(data)
    
    ban_mask = (df['confirmed_ban'] == 1)
    player_mask = (df['confirmed_player'] == 1)
    df_ban = df[ban_mask].copy()
    df_player = df[player_mask].copy()

    dfLocalBan = patron.convertGlobaltoLocal(region_id, df_ban)
    dfLocalReal = patron.convertGlobaltoLocal(region_id, df_player)
    patron.plotheatmap(dfLocalBan, dfLocalReal, region_id, regionTrueName)
    return
