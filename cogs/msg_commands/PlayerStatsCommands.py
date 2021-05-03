from discord.ext.commands import Cog
from discord.ext.commands import command, check

import os
import discord
import aiohttp
from OSRS_Hiscores import Hiscores
import checks
import pandas as pd

import sys
sys.path.append("./utils")
import string_processing

from dotenv import load_dotenv
load_dotenv()
token = os.getenv('API_AUTH_TOKEN')


class PlayerStatsCommands(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="lookup", aliases=["hiscores"])
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


    @command(name="kc", aliases=["killcount"])
    @check(checks.check_allowed_channel)
    async def kc_command(self, ctx, *params):
        playerName = string_processing.joinParams(params)

        if not string_processing.is_valid_rsn(playerName):
            await ctx.channel.send(playerName + " isn't a valid Runescape user name.")
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

                    await ctx.channel.send(msg)
                else:
                    await ctx.channel.send(f"Couldn't grab the !kc for {playerName}")


    @command(name="predict")
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

        if not string_processing.is_valid_rsn(playerName):
            await ctx.channel.send(playerName + " isn't a valid Runescape user name.")
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


    @command(name="excelban")
    @check(checks.check_allowed_channel)
    async def excel_ban_command(self, ctx, *params):
        await self.export_bans(ctx, params, 'excel')

    @command(name="csvban")
    @check(checks.check_allowed_channel)
    async def csv_ban_command(self, ctx, *params):
        await self.export_bans(ctx, params, 'csv')


def setup(bot):
    bot.add_cog(PlayerStatsCommands(bot))