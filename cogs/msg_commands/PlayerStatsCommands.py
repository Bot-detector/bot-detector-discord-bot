from discord.ext.commands import Cog
from discord.ext.commands import command, check, has_permissions

import os
import discord
import aiohttp
import asyncio
from OSRS_Hiscores import Hiscores
from discord.ext.commands.converter import MemberConverter
import checks
import roles
import help_messages
import pandas as pd

import utils.string_processing as string_processing
import utils.discord_processing as discord_processing

from dotenv import load_dotenv
load_dotenv()
token = os.getenv('API_AUTH_TOKEN')


class PlayerStatsCommands(Cog, name='Player Stats Commands'):

    def __init__(self, bot):
        self.bot = bot

    @command(name="lookup", aliases=["hiscores"], description=help_messages.lookup_help_msg)
    @check(checks.check_allowed_channel)
    async def hiscores_lookup(self, ctx, *param):

        rsn = string_processing.joinParams(param)

        if(not string_processing.is_valid_rsn(rsn)):
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
            await ctx.channel.send("Something went terribly wrong. :(")

        await intro_msg.delete()


    @command(name="kc", aliases=["killcount"], description=help_messages.kc_help_msg)
    @check(checks.check_allowed_channel)
    async def kc_command(self, ctx, *params):

        if(len(params) == 0):
            linkedAccounts = await discord_processing.get_linked_accounts(ctx.author.id, token)

            if len(linkedAccounts) == 0:
                mbed = discord.Embed (
                description = f"Please include a player name or use the !link command to pair an OSRS account. "\
                    + "Once you have paired at least once account you will no longer need to type a name."
            )

            await ctx.channel.send(embed=mbed)

            contributions =  await roles.get_multi_player_contributions(linkedAccounts)

            displayName = ctx.author.display_name
            bans = contributions[0]
            possible_bans = contributions[1]
            reports = contributions[2]

            mbed = discord.Embed(title=f"{displayName}'s Stats", color=0x00ff00)

            mbed.add_field (name="Reports Submitted:", value=f"{reports:,d}", inline=False)
            mbed.add_field (name="Possible Bans:", value=f"{possible_bans:,d}", inline=False)
            mbed.add_field (name="Confirmed Bans:", value=f"{bans:,d}", inline=False)
            
            await ctx.channel.send(embed=mbed)

        else:

            playerName = string_processing.joinParams(params)

            if not string_processing.is_valid_rsn(playerName):
                await ctx.channel.send(playerName + " isn't a valid Runescape user name.")
                return

            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.osrsbotdetector.com/api/stats/contributions/" + playerName) as r:
                    if r.status == 200:
                        js = await r.json()
                        reports = int(js['reports'])
                        bans = int(js['bans'])
                        possible_bans = int(js['possible_bans'])

                        mbed = discord.Embed(title=f"{playerName}'s Stats", color=0x00ff00)

                        mbed.add_field (name="Reports Submitted:", value=f"{reports:,d}", inline=False)
                        mbed.add_field (name="Possible Bans:", value=f"{possible_bans:,d}", inline=False)
                        mbed.add_field (name="Confirmed Bans:", value=f"{bans:,d}", inline=False)
            
                        await ctx.channel.send(embed=mbed)
                    else:
                        await ctx.channel.send(f"Couldn't grab the !kc for {playerName}")


    #rank up '/discord/get_linked_accounts/<token>/<discord_id>
    @command(name="rankup", aliases=["updaterank"], description=help_messages.rankup_help_msg)
    @has_permissions(manage_roles = True)
    @check(checks.check_allowed_channel)
    async def rankup_command(self, ctx):
        member = ctx.author

        linkedAccounts = await discord_processing.get_linked_accounts(member.id, token)

        if(len(linkedAccounts) == 0):
            mbed = discord.Embed (
                description = f"You must pair at least one OSRS account with your Discord ID before using this command. Please use the !link command to do so."
            )

            await ctx.channel.send(embed=mbed)
            return
        else:
            for r in member.roles:
                if r.id == roles.special_roles["verified_rsn"]:
                    #awesome, you're verified.
                    break

            else:
                verified_role = discord.utils.find(lambda r: r.id == roles.special_roles["verified_rsn"], member.guild.roles)
                await member.add_roles(verified_role)

        current_role = discord.utils.find(lambda r: 'Bot Hunter' in r.name, member.roles)
        new_role = await roles.get_bot_hunter_role(linkedAccounts, member)

        if(new_role == False):
            mbed = discord.Embed (
                description = f"You currently have no confirmed bans. Keep hunting those bots, and you'll be there in no time! :)"
            )

            await ctx.channel.send(embed=mbed)
            return

        await roles.remove_old_roles(member)
        await member.add_roles(new_role)

        if new_role is not current_role:
            mbed = discord.Embed (
                    description = f"{ctx.author}, you are now a {new_role}!"
                )

            mbed.set_thumbnail(url="https://user-images.githubusercontent.com/45152844/116952387-8ac1fa80-ac58-11eb-8a31-5fe0fc6f5f88.gif")

            await ctx.channel.send(embed=mbed)

        else:
            mbed = discord.Embed (
                    description = f"You are not yet eligible for a new role. I believe in you! So keep going! :)"
                )

            await ctx.channel.send(embed=mbed)
        
        return


    @command(name="predict", description=help_messages.predict_help_msg)
    @check(checks.check_allowed_channel)
    async def predict_command(self, ctx, *params):
        playerName = string_processing.joinParams(params)

        pending_ctx = await ctx.channel.send("Searching the database for the predicted username.")

        if not string_processing.is_valid_rsn(playerName):
            if len(playerName) < 1:
                await ctx.channel.send(f"Please enter a valid Runescape user name.")
                return
            else: 
                await ctx.channel.send(f"{playerName} isn't a valid Runescape user name.")
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
                        + str(string_processing.plus_minus(prediction, 'Real_Player')) + " Prediction: " + str(prediction) + "\n" \
                        + str(string_processing.plus_minus(confidence, 0.75) + " Confidence: " + str(confidence)) + "\n" \
                        + "+" + " ID: " + str(player_id) + "\n" \
                        + "============\n" \
                        + "Prediction Breakdown \n\n"

                    
                    for predict in secondaries:
                        msg += str(string_processing.plus_minus(predict[0], 'Real_Player')) + " " + str(predict[0]) + ": " \
                            + str(predict[1])
                        msg += "\n"

                    msg += "```\n"

                    msg += "Click the reactions below to give feedback on the above prediction:"
                        
                    my_msg = await ctx.channel.send(msg)

                    await my_msg.add_reaction('✔️')
                    await my_msg.add_reaction('❌')

                else:
                    await ctx.channel.send(f"I couldn't get a prediction for {playerName} :(")
                    return

        await pending_ctx.delete()

    async def export_bans(self, ctx, params, filetype):
        playerName = string_processing.joinParams(params)
        discord_id = ctx.author.id

        if not string_processing.is_valid_rsn(playerName):
            await ctx.channel.send(playerName + " isn't a valid Runescape user name.")
            return

        status = await discord_processing.get_player_verification_full_status(playerName=playerName, token=token)

        if status is None:
            await ctx.channel.send("Please verify your ownership of: '" +  playerName + "'. Type `!link " + playerName + "' in this channel.")
            return

        owner_id = status['Discord_id']
        verified = status['Verified_status']

        if discord_id != owner_id:
            await ctx.channel.send("Please verify your ownership of: '" +  playerName + "'. Type `!link " + playerName + "' in this channel.")
            return
        
        if verified == 0:
            await ctx.channel.send("You must complete the verification process for: '" + playerName + "'. Please check your DMs for a previously sent verification token.")
            return

        info_msg = await ctx.channel.send("Getting that data for you right now! One moment, please :)")

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.osrsbotdetector.com/dev/discord/player_bans/{token}/{playerName}") as r:
                if r.status == 200:

                    js = await r.json()
                    df = pd.DataFrame(js)

                    if filetype == 'excel':
                        df.to_excel(f"{playerName}_bans.xlsx")
                        filePath = f'{os.getcwd()}/{playerName}_bans.xlsx'
                    else:
                        df.to_csv(f"{playerName}_bans.csv")
                        filePath = f'{os.getcwd()}/{playerName}_bans.csv'

                    await ctx.author.send(file=discord.File(filePath))
                    os.remove(filePath)
                    await info_msg.edit(content=f"Your {filetype} file for {playerName} has been sent to your DMs.")
                else:
                    await info_msg.edit(content=f"Could not grab the banned bots {filetype} file for {playerName}.")


    @command(name="excelban", aliases=["excelbans"], description=help_messages.excelban_help_msg)
    @check(checks.check_allowed_channel)
    async def excel_ban_command(self, ctx, *params):
        await self.export_bans(ctx, params, 'excel')

    @command(name="csvban", aliases=["csvbans"], description=help_messages.csvban_help_msg)
    @check(checks.check_allowed_channel)
    async def csv_ban_command(self, ctx, *params):
        await self.export_bans(ctx, params, 'csv')


def setup(bot):
    bot.add_cog(PlayerStatsCommands(bot))