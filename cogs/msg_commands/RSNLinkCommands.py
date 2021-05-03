from discord.ext.commands import Cog
from discord.ext.commands import command, check

import re
import os
import aiohttp
import string
import random
import sql
import checks
import sys
sys.path.append("./utils")
import string_processing

from dotenv import load_dotenv
load_dotenv()
token = os.getenv('API_AUTH_TOKEN')

class RSNLinkCommands(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="link")
    @check(checks.check_allowed_channel)
    async def link_command(self,ctx, *player_name):

        joinedName = string_processing.joinParams(player_name)

        if not string_processing.is_valid_rsn(joinedName):
            await ctx.channel.send(joinedName  + " isn't a valid Runescape user name.")
            return

        code = string_processing.id_generator()
        discord_id = ctx.author.id


        msgPassed = "```diff" + "\n" \
                    + "====== STATUS ======\n" \
                    + f"Request to link RSN: {player_name} \n" \
                    + f"Your discord ID is: {discord_id} \n" \
                    + f"Access Code: {code} \n" \
                    + "====== SETUP ======\n" \
                    + "+ Please read through these instructions." + "\n" \
                    + "+ 1. Open Old School Runescape through RuneLite." + "\n" \
                    + f"+ 2. Login as: '{player_name}' \n" \
                    + "+ 3. Join the clan channel: 'Ferrariic'." + "\n" \
                    + "+ 4. Verify that a Plugin Admin or Plugin Moderator is present in the channel." + "\n" \
                    + "+ 5. If a Plugin Admin or Plugin Moderator is not available, please leave a message in #bot-commands." + "\n" \
                    + f"+ 6. Type into the Clan Chat: '!Code {code}' \n" \
                    + f"+ 7. Type '!verify {player_name}' in #bot-commands channel to confirm that you have been Verified." + "\n" \
                    + "+ 8. Verification Process Complete." + "\n" \
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
                    + f"+ Player: {player_name} \n" \
                    + "====== Verification Information ======\n" \
                    + "+ Player is: Verified." + "\n" \
                    + "```"


        verifyID = await self.get_playerid_verification(playerName=player_name, token=token)


        if verifyID == None:
            await ctx.author.send(msgInstallPlugin)
            return


        verifyStatus = await self.get_player_verification_full_status(playerName=player_name, token=token)
        if verifyStatus == None:
            return
        else:
            
            isVerified = verifyStatus['Verified_status']

            if isVerified == 1:
                owner_verified_info = await self.get_verified_player_info(playerName=player_name, token=token)
                ownerID = owner_verified_info['Discord_id']
                if ownerID == discord_id:
                    ctx.author.send(msgVerified)
                    return

        try:
            messagetxt = await self.post_discord_player_info(discord_id=discord_id, player_id=verifyID, code=code, token=token)
            print(messagetxt)
            await ctx.author.send(msgPassed)
        except Exception as e:
            pass

        await ctx.author.send("Nice.")
            

    async def get_player_verification_full_status(playerName, token):

        url = f'https://www.osrsbotdetector.com/dev/discord/verify/player_rsn_discord_account_status/{token}/name'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    data = await r.json()

        try:
            return data[0]
        except:
            return None

    async def get_playerid_verification(playerName, token):

        url = f'https://www.osrsbotdetector.com/dev/discord/verify/playerid/{token}/{playerName}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    playerIDverif = await r.json()

        try:
            return playerIDverif[0]
        except:
            return None

    async def get_verified_player_info(playerName, token):

        url = f'https://www.osrsbotdetector.com/dev/discord/verify/verified_player_info/{token}/{playerName}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    vplayerinfo = await r.json()

        return vplayerinfo[0]

    async def post_discord_player_info(discord_id, player_id, code, token):

        id = player_id['id']

        url = f'https://www.osrsbotdetector.com/dev/discord/verify/insert_player_dpc/{token}/{discord_id}/{id}/{code}'

        async with aiohttp.ClientSession() as session:
            async with session.post(url) as r:
                return await r.json() if r.status == 200 else {"error":f"Failed: {r.status} error"}

    @command(name="verify")
    @check(checks.check_allowed_channel)
    async def verify_comand(self, ctx, *player_name):

        joinedName = string_processing.joinParams(player_name)

        if not string_processing.is_valid_rsn(joinedName):
            await ctx.channel.send(joinedName + " isn't a valid Runescape user name.")
            return

        msgVerified = "```diff" + "\n" \
                    + "+ Player: " + str(joinedName) + "\n" \
                    + "====== Verification Information ======\n" \
                    + "+ Player is: Verified." + "\n" \
                    + "```"

        msgUnverified = "```diff" + "\n" \
                        + "+ Player: " + str(joinedName) + "\n" \
                        + "====== Verification Information ======\n" \
                        + "- Player is: Unverified." + "\n" \
                        + f"- Please use the !link {joinedName} command to claim ownership." + "\n" \
                        + "```"
        try:
            verified = await self.get_player_verified_status(joinedName)
        except IndexError:
            verified = 0

        if verified:
            msg = msgVerified
        else:
            msg = msgUnverified

        await ctx.channel.send(msg)

    async def get_player_verified_status(self, player_name):

        url = f'https://www.osrsbotdetector.com/dev/discord/player_verification_status/{token}/{player_name}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    verify = await r.json()

        return verify[0]['Verified_status']

def setup(bot):
    bot.add_cog(RSNLinkCommands(bot))






