import os
import random
import re
import string
from datetime import datetime, timezone
from random import randint
from OSRS_Hiscores import Hiscores

import discord
import aiohttp
import pandas as pd

import patron
import sql
import json
import numpy

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('API_AUTH_TOKEN')

# Fun Commands

async def poke_command(message):
    await message.channel.send('Teehee! :3')

async def meow_command(message):
    url = "https://cataas.com/cat/gif?json=true" if randint(0, 1) > 0 else "https://cataas.com/cat?json=true"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                await message.channel.send("https://cataas.com" + js['url'])
            else:
                await message.channel.send("Ouw souwce fo' cats am cuwwentwy down, sowwy :3")


async def woof_command(message):
    url = "https://some-random-api.ml/img/dog"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                await message.channel.send(js['link'])
            else:
                await message.channel.send("Who let the dogs out?")


async def birb_command(message):
    url = "http://shibe.online/api/birds"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                await message.channel.send(js[0])
            else:
                await message.channel.send("Birds all flew away. :(")


async def bunny_command(message):
    url = "https://api.bunnies.io/v2/loop/random/?media=gif,png"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                await message.channel.send(js['media']['gif'])
            else:
                await message.channel.send("The buns went on the run.")


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

async def beta_command(message):
    await message.channel.send('https://github.com/Bot-detector/bot-detector/wiki/Running-the-Development-Version-From-Source')


async def patreon_command(message):
    await message.channel.send('https://www.patreon.com/bot_detector')


async def hiscores_lookup(ctx, rsn):
    if(not is_valid_rsn(rsn)):
        await ctx.channel.send(rsn + " is not a valid RSN")
        return

    try:
        username = rsn
        username_parsed = username.replace(" ", "_")
        intro_msg = await ctx.send("Searching for User... If there is no response, there was no account found.")
        user = Hiscores(username_parsed, 'N')

        skills_list = [ 'Attack',           'Hitpoints',    'Mining', 
                        'Strength',         'Agility',      'Smithing',
                        'Defense',          'Herblore',     'Fishing',
                        'Ranged',           'Thieving',     'Cooking',
                        'Prayer',           'Crafting',     'Firemaking',
                        'Magic',            'Fletching',    'Woodcutting',
                        'Runecrafting',     'Slayer',       'Farming',
                        'Construction',     'Hunter',       'Total' ]

        embedvar = discord.Embed(title=username, description="OSRS Hiscores Lookup", color=0x00ff00)

        for skill in skills_list:
            embedvar.add_field( name=f"{skill} - {user.skill(skill.lower())}", 
                                value=f"EXP - {int(user.skill(skill.lower(), 'experience')):,d}", 
                                inline=True )
        
        await ctx.channel.send(embed=embedvar)


    except Exception as e:
        print(e)
        await ctx.channel.send("Something went terribly wrong. :(")

    await intro_msg.delete()


async def github_command(message, repo):
    repos = {
        "core": "https://github.com/Ferrariic/Bot-Detector-Core-Files",
        "plugin": "https://github.com/Ferrariic/bot-detector"
    }

    not_found_text = f"{repo} isn't a valid GitHub repository name. Try 'Core' or 'Plugin'."

    repo_url = repos.get(repo.lower(), not_found_text)

    await message.channel.send(repo_url)


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

    await message.channel.send(msg)


async def kc_command(message, params):
    playerName = params

    if not is_valid_rsn(playerName):
        await message.channel.send(playerName + " isn't a valid Runescape user name.")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.osrsbotdetector.com/api/stats/contributions/" + playerName) as r:
            if r.status == 200:
                js = await r.json()
                reports = js['reports']
                bans = js['bans']
                possible_bans = js['possible_bans']

                msg = "```" + playerName + "'s Stats: \n" \
                    + "Reports Submitted: " + str(reports) + "\n" \
                    + "Probable/Pending Bans: " + str(possible_bans) + "\n" \
                    + "Confirmed Bans: " + str(bans) + "```\n"

                await message.channel.send(msg)
            else:
                await message.channel.send(f"Couldn't grab the !kc for {playerName}")


async def predict_command(message, params):
    playerName = params

    pending_message = await message.channel.send("Searching the database for the predicted username.")

    if not is_valid_rsn(playerName):
        if len(playerName) < 1:
            await message.channel.send(f"Please enter a valid Runescape user name.")
            return
        else: 
            await message.channel.send(f"{playerName} isn't a valid Runescape user name.")
            return

    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.osrsbotdetector.com/api/site/prediction/" + playerName) as r:
            if r.status == 200:
                js = await r.json()
                name =        js['player_name']
                prediction =  js['prediction_label']
                player_id =   js['player_id']
                confidence =  js['prediction_confidence']
                secondaries = js['secondary_predictions']

                msg = "```diff\n" \
                    + "+" + " Name: " + str(name) + "\n" \
                    + str(plus_minus(prediction, 'Real_Player')) + " Prediction: " + str(prediction) + "\n" \
                    + str(plus_minus(confidence, 0.75) + " Confidence: " + str(confidence)) + "\n" \
                    + "+" + " ID: " + str(player_id) + "\n" \
                    + "============\n" \
                    + "Prediction Breakdown \n\n"

                
                for predict in secondaries:
                    print("poop")
                    print(predict)
                    msg += str(plus_minus(predict[0], 'Real_Player')) + " " + str(predict[0]) + ": " \
                        + str(predict[1])
                    msg += "\n"


                msg += "```\n"

                msg += "Click the reactions below to give feedback on the above prediction:"
                    
                my_msg = await message.channel.send(msg)

                await my_msg.add_reaction('✔️')
                await my_msg.add_reaction('❌')

            else:
                await message.channel.send(f"I couldn't get a prediction for {playerName} :(")
                return

    await pending_message.delete()


# Heatmap and Region Commands

async def region_command(message, params, token):
    regionName = params
    dataRegion = await patron.getHeatmapRegion(regionName, token)
    dfDataRegion = pd.DataFrame(dataRegion)
    dfRegion = patron.displayDuplicates(dfDataRegion)
    
    if len(dfRegion) < 30:
        regionTrueName, region_id = patron.Autofill(dfRegion, regionName)
        
        msg = "```diff" + "\n" \
              + "+ Input: " + str(regionName) + "\n" \
              + "+ Selection From: " + str(', '.join([str(elem) for elem in dfRegion['region_name'].values])) + "\n" \
              + "+ Selected: " + str(regionTrueName) + "\n" \
              + "```"
    else:
        msg = "```diff" + "\n" \
              + "- More than 30 Regions selected. Please refine your search." + "\n" \
              + "```"
    await message.channel.send(msg)


# Patron Heatmap command

async def heatmap_command(message, params, token):

    info_msg = await message.channel.send("Getting that map ready for you. One moment, please!")

    regionName = params
  
    dataRegion = await patron.getHeatmapRegion(regionName, token)
    dfDataRegion = pd.DataFrame(dataRegion)
    dfRegion = patron.displayDuplicates(dfDataRegion)

    if len(dfRegion)<30:
        regionTrueName, region_id = patron.Autofill(dfRegion, regionName)

        mapWasGenerated = await runAnalysis(regionTrueName, region_id)

        if not mapWasGenerated:
            await map_command(message, params)
            await message.channel.send("We have no data on this region yet.")

        else:
            try:
                await message.channel.send(file=discord.File(f'{os.getcwd()}/{region_id}.png'))
                await patron.CleanupImages(region_id)

            except:
                await message.channel.send("Uhhh... I should have a heatmap to give you, but I don't. Please accept this image of a cat fixing our bot instead.")
                await message.channel.send('https://i.redd.it/lel3o4e2hhp11.jpg')

    else:
        msg = ">30 Regions selected. Please refine your search."
        await message.channel.send(msg)

    
    await info_msg.delete()

    
async def map_command(message, params):

    if params.isdigit():
        region_id = params

        msg = str(
            'https://raw.githubusercontent.com/Ferrariic/OSRS-Visible-Region-Images/main/Region_Maps/{}.png'.format(region_id))

    else:
        regionName = params
        dataRegion = await patron.getHeatmapRegion(regionName, token)
        dfDataRegion = pd.DataFrame(dataRegion)
        dfRegion = patron.displayDuplicates(dfDataRegion)
    
        if len(dfRegion) < 30:
            regionTrueName, region_id = patron.Autofill(dfRegion, regionName)
            msg = str(
                'https://raw.githubusercontent.com/Ferrariic/OSRS-Visible-Region-Images/main/Region_Maps/{}.png'.format(region_id))
        else:
            msg = "```diff" + "\n" \
                + "- More than 30 Regions selected. Please refine your search." + "\n" \
                + "```"
        
    await message.channel.send(msg)


async def coords_command(message, x, y, z, zoom):

    BASE_URL = "https://raw.githubusercontent.com/Explv/osrs_map_tiles/master/"

    msg = BASE_URL + str(z) + "/" + str(zoom) + "/" + str(y) + "/" + str(x) + ".png"

    await message.channel.send(msg)


# Database Commands

async def submit_command(message, paste_url, recipient):
    errors = "No Errors"

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

    try:
        paste_soup = sql.get_paste_data(paste_url)
        List = sql.get_paste_names(paste_soup)
        labelCheck = sql.get_paste_label(paste_soup)
        sql.execute_sql(sqlLabelInsert, insert=True, param=[labelCheck])
        sql.InsertPlayers(sqlPlayersInsert, List)
        dfLabelID = pd.DataFrame(sql.execute_sql(sqlLabelID, insert=False, param=[labelCheck]))
        playerID = sql.PlayerID(sqlPlayerID, List)
        sql.InsertPlayerLabel(sqlInsertPlayerLabel, playerID, dfLabelID)
    except Exception as e:
        errors = str(e)

    msg = "```diff" + "\n" \
          + "Paste Information Submitted" + "\n" \
          + "_____________________" + "\n" \
          + "+ Link: " + str(paste_url) + "\n" \
          + "+ Errors: " + str(errors) + "\n" \
          + "```"

    await recipient.send(msg)


async def primary_command(message, player_name):
    discord_id = message.author.id

    if not is_valid_rsn(player_name):
        await message.channel.send(player_name + " isn't a valid Runescape user name.")
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

    player_id, exists = sql.verificationPull(player_name)
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
                    print(
                        "The account you are attempting to link is Unverified. Please !link <RSN> and verify this account.")
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


async def link_command(message, player_name):
    if not is_valid_rsn(player_name):
        await message.channel.send(player_name + " isn't a valid Runescape user name.")
        return

    owner_id = 0
    code = id_generator()
    discord_id = message.author.id

    msgPassed = "```diff" + "\n" \
                + "====== STATUS ======\n" \
                + "Request to link RSN: " + str(player_name) + "\n" \
                + "Your discord ID is: " + str(discord_id) + "\n" \
                + "Access Code: " + str(code) + "\n" \
                + "====== SETUP ======\n" \
                + "+ Please read through these instructions." + "\n" \
                + "+ 1. Open Old School Runescape through RuneLite." + "\n" \
                + "+ 2. Login as: '" + str(player_name) + "'." + "\n" \
                + "+ 3. Join the clan channel: 'Ferrariic'." + "\n" \
                + "+ 4. Verify that a Plugin Admin or Plugin Moderator is present in the channel." + "\n" \
                + "+ 5. If a Plugin Admin or Plugin Moderator is not available, please leave a message in #bot-commands." + "\n" \
                + "+ 6. Type into the Clan Chat: '!Code " + str(code) + "'." + "\n" \
                + "+ 7. Type '!verify " + str(
        player_name) + "' in #bot-commands channel to confirm that you have been Verified." + "\n" \
                + "+ 9. Verification Process Complete." + "\n" \
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
                  + "+ Player: " + str(player_name) + "\n" \
                  + "====== Verification Information ======\n" \
                  + "+ Player is: Verified." + "\n" \
                  + "```"

    msgUnverified = "```diff" + "\n" \
                    + "+ Player: " + str(player_name) + "\n" \
                    + "====== Verification Information ======\n" \
                    + "- Player is: Unverified." + "\n" \
                    + f"- Please use the !link {player_name} command to claim ownership." + "\n" \
                    + "```"

    player_id, exists = sql.verificationPull(player_name)
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


async def verify_comand(message, player_name):
    if not is_valid_rsn(player_name):
        await message.channel.send(player_name + " isn't a valid Runescape user name.")
        return

    msgVerified = "```diff" + "\n" \
                  + "+ Player: " + str(player_name) + "\n" \
                  + "====== Verification Information ======\n" \
                  + "+ Player is: Verified." + "\n" \
                  + "```"

    msgUnverified = "```diff" + "\n" \
                    + "+ Player: " + str(player_name) + "\n" \
                    + "====== Verification Information ======\n" \
                    + "- Player is: Unverified." + "\n" \
                    + f"- Please use the !link {player_name} command to claim ownership." + "\n" \
                    + "```"

    player_id, exists = sql.verificationPull(player_name)
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
    if (isinstance(var, float)):
        if (var > compare):
            diff_control = '+'
    if (isinstance(var, str)):
        if (str(var) == str(compare)):
            diff_control = '+'
    return diff_control


# Analysis run for Patron Heatmap
async def runAnalysis(regionTrueName, region_id):
    region_id = int(region_id)
    data = await patron.getHeatmapData(region_id, token)
    df = pd.DataFrame(data)

    if(df.empty):
        return False

    if 'confirmed_ban' in df.columns:
        ban_mask = (df['confirmed_ban'] == 1)
        df_ban = df[ban_mask].copy()
        dfLocalBan = patron.convertGlobaltoLocal(region_id, df_ban)

    else:
        dfLocalBan = pd.DataFrame()


    if 'confirmed_player' in df.columns:
        player_mask = (df['confirmed_player'] == 1)
        df_player = df[player_mask].copy()
        dfLocalReal = patron.convertGlobaltoLocal(region_id, df_player)

    else:
        dfLocalReal = pd.DataFrame()
        
    if not dfLocalBan.empty and not dfLocalReal.empty:
        patron.plotheatmap(dfLocalBan, dfLocalReal, region_id, regionTrueName)

    else:
        return False


    return True
