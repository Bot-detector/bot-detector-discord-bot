from discord.ext.commands import Cog
from discord.ext.commands import command, check

import re
import os
import aiohttp
import string
import random
import help_messages
import checks
import discord

import utils.string_processing as string_processing
import utils.discord_processing as discord_processing

from dotenv import load_dotenv
load_dotenv()
token = os.getenv('API_AUTH_TOKEN')

class RSNLinkCommands(Cog, name='RSN Link Commands'):

    def __init__(self, bot):
        self.bot = bot

    @command(name="link", aliases=["pair"], description=help_messages.link_help_msg)
    @check(checks.check_allowed_channel)
    async def link_command(self ,ctx, *player_name):

        if len(player_name) == 0:
            await ctx.channel.send("Please specify the RSN of the account you'd wish to link. !link <RSN>")
            return

        joinedName = string_processing.joinParams(player_name)

        if not string_processing.is_valid_rsn(joinedName):
            await ctx.channel.send(joinedName  + " isn't a valid Runescape user name.")
            return

        code = string_processing.id_generator()
        discord_id = ctx.author.id

        verifyID = await discord_processing.get_playerid_verification(playerName=joinedName, token=token)

        if verifyID == None:
            mbed = await installplugin_msg()
            await ctx.channel.send(embed=mbed)
            return

        verifyStatus = await discord_processing.get_player_verification_full_status(playerName=joinedName, token=token)

        if len(verifyStatus) == 0:
            pass
        else:
            for status in verifyStatus:
                if int(status['Verified_status']) == 1:
                    isVerified = 1
                    break
            else:
                isVerified = 0

            if isVerified == 1:
                owner_verified_info = await discord_processing.get_verified_player_info(playerName=joinedName, token=token)
                ownerID = owner_verified_info['Discord_id']
                if ownerID == discord_id:
                    mbed = await verified_msg(joinedName)
                    await ctx.channel.send(embed=mbed)
                    return

        try:
            await discord_processing.post_discord_player_info(discord_id=discord_id, player_id=verifyID, code=code, token=token)
            mbed = await link_msg(joinedName=joinedName, code=code)
            await ctx.author.send(embed=mbed)
        except Exception as e:
            print(e)
            pass


    @command(name="verify", description=help_messages.verify_help_msg)
    @check(checks.check_allowed_channel)
    async def verify_comand(self, ctx, *player_name):

        if len(player_name) == 0:
            await ctx.channel.send("Please specify the RSN of the account you'd wish to view the verification status for. !verify <RSN>")
            return

        joinedName = string_processing.joinParams(player_name)

        if not string_processing.is_valid_rsn(joinedName):
            await ctx.channel.send(joinedName + " isn't a valid Runescape user name.")
            return

        verifyStatus = await discord_processing.get_player_verification_full_status(playerName=joinedName, token=token)

        try:
            for status in verifyStatus:
                if int(status['Verified_status']) == 1:
                    isVerified = True
                    break
            else:
                isVerified = False

            if isVerified:
                mbed = await verified_msg(joinedName)
            else:
                mbed = await unverified_msg(joinedName)
        except:
            mbed = await unverified_msg(joinedName)

        await ctx.channel.send(embed=mbed)

    @command(name="linked", aliases=["getlinks"], description=help_messages.linked_help_msg)
    @check(checks.check_allowed_channel)
    async def linked_comand(self, ctx):
        linkedAccounts = await discord_processing.get_linked_accounts(ctx.author.id, token)

        if len(linkedAccounts) == 0:
            await ctx.author.send("You do not have any OSRS accounts linked to this Discord ID. Use the !link command in order to link an account.")
        else:
            mbed = discord.Embed(color=0x00ff00)

            names = ""
            for acc in linkedAccounts:
                names += f"{acc['name']}\n"
                

            mbed.add_field (name="Linked Accounts:", value=f"{names}", inline=False)

            await ctx.author.send(embed=mbed)

        return

async def verified_msg(joinedName):
    mbed = discord.Embed(title=f"{joinedName}'s Status:", color=0x00ff00)
    mbed.add_field (name="Verified:", value=f"{joinedName} is Verified.", inline=False)
    mbed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117238120-538b4f00-adfa-11eb-9c58-d5500af7d215.png")
    return mbed


async def unverified_msg(joinedName):
    mbed = discord.Embed(title=f"{joinedName}'s Status:", color=0xff0000)
    mbed.add_field (name="Unverified:", value=f"{joinedName} is Unverified.", inline=False)
    mbed.add_field (name="Next Steps:", value=f"Please type '!link {joinedName}'", inline=False)
    mbed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117239076-19bb4800-adfc-11eb-94c4-27ff7e1217cc.png")
    return mbed


async def installplugin_msg():
    mbed = discord.Embed(title=f"User Not Found:", color=0xff0000)
    mbed.add_field (name="Status:", value=f"No reports exist from specified player.", inline=False)
    mbed.add_field (name="Next Steps:", value=f"Please install the Bot-Detector Plugin on RuneLite if you have not done so.\n\n" \
        + "If you have the plugin installed, you will need to disable Anonymous Reporting for us to be able to !link your account.", inline=False)
    mbed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117361316-e1f9e200-ae87-11eb-840b-3bad75e80ff6.png")
    return mbed


async def link_msg(joinedName, code):
    mbed = discord.Embed(title=f"Linking '{joinedName}'':", color=0x0000ff)

    mbed.add_field (name="STATUS", value=f"Request to link '{joinedName}'." + "\n" \
        + f"Access Code: {code}", inline=False)

    mbed.add_field (name="SETUP", value=f"Please read through these instructions." + "\n" \
        + f"1. Open Old School Runescape through RuneLite." + "\n" \
        + f"2. Login as: '{joinedName}'" + "\n" \
        + f"3. Join the clan channel: 'Ferrariic'." + "\n" \
        + f"4. Verify that a Plugin Admin or Plugin Moderator is present in the channel." + "\n" \
        + f"5. If a Plugin Admin or Plugin Moderator is not available, please leave a message in #bot-detector-commands." + "\n" \
        + f"6. Type into the Clan Chat: '!Code {code}'." + "\n" \
        + f"7. Type '!verify {joinedName}' in #bot-commands channel to confirm that you have been Verified." + "\n" \
        + f"8. Verification Process Complete.", inline=False)

    mbed.add_field (name="INFO", value=f"You may link multiple Runescape accounts via this method." + "\n" \
        + f"1. If you change the name of your account(s) you must repeat this process with your new RSN(s)." + "\n" \
        + f"2. In the event of a name change please allow some time for your data to be transferred over.", inline=False)

    mbed.add_field (name="NOTICE", value=f"Do not delete this message." + "\n" \
        + f"1. If this RSN was submitted in error, please type '!link <Your Correct RSN>'." + "\n" \
        + f"2. This code will not expire, it is tied to your unique RSN:Discord Pair." + "\n" \
        + f"3. If you are unable to become 'Verified' through this process, please contact an administrator for assistance.", inline=False)
    return mbed

def setup(bot):
    bot.add_cog(RSNLinkCommands(bot))