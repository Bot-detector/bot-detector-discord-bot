import os
from inspect import cleandoc

import json
import discord
import zipfile as zip
from discord.ext import commands
from dotenv import load_dotenv
from OSRS_Hiscores import Hiscores

import help_messages
import utils
from utils import discord_processing, roles, check_allowed_channel


load_dotenv()
token = os.getenv('API_AUTH_TOKEN')

class PlayerStatsCommands(utils.CommonCog, name='Player Stats Commands'):
    cog_check = check_allowed_channel

    @commands.command(aliases=["hiscores"], description=help_messages.lookup_help_msg)
    async def lookup(self, ctx, *, username):
        if not utils.is_valid_rsn(username):
            return await ctx.send(f"{username} is not a valid RSN")

        try:
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

            embed = discord.Embed(title=username, description="OSRS Hiscores Lookup", color=0x00ff00)

            for skill in skills_list:
                embed.add_field(name=f"{skill} - {user.skill(skill.lower())}",
                                   value=f"EXP - {int(user.skill(skill.lower(), 'experience')):,d}",
                                   inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send("Something went terribly wrong. :(")
            raise e

        await intro_msg.delete()


    @commands.command(aliases=["killcount"], description=help_messages.kc_help_msg)
    async def kc(self, ctx, *, player_name=None):
        await ctx.trigger_typing()
        if not player_name:
            linkedAccounts = await discord_processing.get_linked_accounts(self.bot.session, ctx.author.id, token)

            if not linkedAccounts:
                embed = discord.Embed(
                    description=cleandoc(f"""
                        Please include a player name or use the !link command to pair an OSRS account.
                        Once you have paired at least one account you will no longer need to type a name.
                    """)
                )

                return await ctx.send(embed=embed)

            async with self.bot.session.get(url="https://www.osrsbotdetector.com/api/stats/contributions/", json=json.dumps(linkedAccounts)) as r:
                if r.status != 200:
                    return await ctx.send(f"Couldn't grab the !kc for {ctx.author.display_name}")

                js = await r.json()

            manual_reports = int(js['manual']['reports'])
            manual_bans = int(js['manual']['bans'])
            manual_incorrect = int(js['manual']['incorrect_reports'])

            total_reports = int(js['total']['reports'])
            total_bans = int(js['total']['bans'])
            total_possible_bans = int(js['total']['possible_bans'])

            embed = discord.Embed(title=f"{ctx.author.display_name}'s Stats", color=0x00ff00)

        elif utils.is_valid_rsn(player_name):
            async with self.bot.session.get(f"https://www.osrsbotdetector.com/api/stats/contributions/{player_name}") as r:
                if r.status != 200:
                    return await ctx.send(f"Couldn't grab the !kc for {player_name}")

                js = await r.json()

            manual_reports = int(js['manual']['reports'])
            manual_bans = int(js['manual']['bans'])
            manual_incorrect = int(js['manual']['incorrect_reports'])

            total_reports = int(js['total']['reports'])
            total_bans = int(js['total']['bans'])
            total_possible_bans = int(js['total']['possible_bans'])

            embed = discord.Embed(title=f"{player_name}'s Stats", color=0x00ff00)
        else:
            return await ctx.send(f"{player_name} isn't a valid Runescape user name.")

        if manual_reports == 0:
            report_accuracy = None
        elif manual_incorrect == 0:
            report_accuracy = 100.00
        else:
            report_accuracy = round((manual_bans / (manual_bans + manual_incorrect)) * 100, 2)

        embed.add_field(name="Reports Submitted:", value=f"{total_reports:,d}", inline=False)
        embed.add_field(name="Possible Bans:", value=f"{total_possible_bans:,d}", inline=False)
        embed.add_field(name="Confirmed Bans:", value=f"{total_bans:,d}", inline=False)

        if report_accuracy is not None:
            embed.add_field(name="Manual Flags:", value=f"{manual_reports:,d}", inline=False)
            embed.add_field(name="Manual Flag Accuracy:", value=f"{report_accuracy}%", inline=False)

        embed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117364618-212a3200-ae8c-11eb-8b42-9ef5e225930d.gif")

        if total_reports == 0:
            embed.set_footer(text="If you have the plugin installed but are not seeing your KC increase\nyou may have to disable Anonymous Mode in your plugin settings.",
            icon_url="https://raw.githubusercontent.com/Bot-detector/bot-detector/master/src/main/resources/warning.png")

        await ctx.send(embed=embed)


    #rank up '/discord/get_linked_accounts/<token>/<discord_id>
    @commands.command(aliases=["updaterank"], description=help_messages.rankup_help_msg)
    async def rankup(self, ctx):
        await ctx.trigger_typing()
        member = ctx.author
        linkedAccounts = await discord_processing.get_linked_accounts(self.bot.session, member.id, token)

        if not len(linkedAccounts):
            embed = discord.Embed (
                description = "You must pair at least one OSRS account with your Discord ID before using this command. Please use the !link command to do so.",
                color = discord.Colour.dark_red()
            )

            return await ctx.send(embed=embed)

        for r in member.roles:
            if r.id == roles.special_roles["Discord-RSN Linked"]["role_id"]:
                #awesome, you're verified.
                break

        else:
            verified_role = discord.utils.find(lambda r: r.id == roles.special_roles["Discord-RSN Linked"]["role_id"], member.guild.roles)
            await member.add_roles(verified_role)

        current_role = discord.utils.find(lambda r: 'Bot Hunter' in r.name, member.roles)
        new_role, current_amount, next_role_amount = await roles.get_bot_hunter_role(self.bot.session, linkedAccounts, member)

        if new_role is False:
            embed = discord.Embed(
                description = "You currently have no confirmed bans. Keep hunting those bots, and you'll be there in no time! :)",
                color = discord.Colour.dark_red()
            )

            return await ctx.send(embed=embed)

        await roles.remove_old_roles(member)
        await member.add_roles(new_role)

        if new_role == current_role:
            embed = discord.Embed(
                    description = f"You are not yet eligible for a new role. Only **{next_role_amount - current_amount}** more confirmed bans and you'll be there! :D",
                    color = new_role.color
            )

            return await ctx.send(embed=embed)

        embed = discord.Embed(
            description=f"{ctx.author.display_name}, you are now a {new_role}!",
            color=new_role.color
        )

        embed.set_thumbnail(url="https://user-images.githubusercontent.com/45152844/116952387-8ac1fa80-ac58-11eb-8a31-5fe0fc6f5f88.gif")
        await ctx.send(embed=embed)



    @commands.command(aliases=["detect"], description=help_messages.predict_help_msg)
    async def predict(self, ctx, *, player_name):

        pending_msg = await ctx.send("Searching the database for the predicted username.")
        await ctx.trigger_typing()

        if not utils.is_valid_rsn(player_name):
            if len(player_name) < 1:
                await ctx.send(f"Please enter a valid Runescape user name.")
                return
            else:
                await ctx.send(f"{player_name} isn't a valid Runescape user name.")
                return

        async with self.bot.session.get(f"https://www.osrsbotdetector.com/api/site/prediction/{player_name}") as r:
            if r.status != 200:
                return await ctx.send(f"I couldn't get a prediction for {player_name} :(")

            js = await r.json()

        name =        js['player_name']
        prediction =  js['prediction_label']
        player_id =   js['player_id']
        confidence =  js['prediction_confidence']
        secondaries = js['secondary_predictions']

        msg = cleandoc(f"""```diff
            + Name: {name}
            {utils.plus_minus(prediction, 'Real_Player')} Prediction: {prediction}
            {utils.plus_minus(confidence, 0.75)} Confidence: {confidence * 100:.2f}%
            + ID: {player_id}
            ============
            Prediction Breakdown
        """)

        msg += "\n"

        for predict in secondaries:
            msg += cleandoc(f"""
                {utils.plus_minus(predict[0], 'Real_Player')} {predict[0]}: {predict[1] * 100:.2f}%
            """)

            msg += "\n"

        msg += "```"

        await pending_msg.delete()
        await ctx.send(msg)

        #TODO Add back in the feedback reactions. Right now I can only get the first one added to load.

    async def export_bans(self, ctx, file_type):
        discord_id = ctx.author.id

        req_payload = {
            "discord_id": discord_id,
            "display_name": ctx.author.display_name
        }

        info_msg = await ctx.send("Getting that data for you right now! One moment, please :)")

        async with self.bot.session.get(
            url=f"https://www.osrsbotdetector.com/api/discord/player_bans/{token}", 
            json=json.dumps(req_payload)) as r:

            if r.status != 200:
                js = await r.json()
                await info_msg.delete()
                return await ctx.reply(f"{js['error']}")
            else:
                file_name = f"{ctx.author.display_name}_bans"

                with open(file=file_name+".xlsx", mode="wb") as out_file:
                    while True:
                        chunk = await r.content.read(100)
                        if not chunk:
                            break
                        out_file.write(chunk)
                
                with zip.ZipFile(file_name+".zip", "w") as ban_zip:
                    ban_zip.write(filename=file_name+".xlsx", compress_type=zip.ZIP_DEFLATED)

            await ctx.author.send(file=discord.File(file_name+".zip"))

            os.remove(file_name+".xlsx")
            os.remove(file_name+".zip")

            await info_msg.delete()
            await ctx.reply(f"Your bans export has been sent to your DMs.")


    @commands.command(aliases=["excelbans", "bansexport"], description=help_messages.excelban_help_msg)
    async def excelban(self, ctx):
        await self.export_bans(ctx, 'excel')

    ''' TODO: Add back in selection between excel and csv outputs
    @commands.command(aliases=["csvbans"], description=help_messages.csvban_help_msg)
    async def csvban(self, ctx):
        await self.export_bans(ctx, 'csv')
    '''


def setup(bot):
    bot.add_cog(PlayerStatsCommands(bot))
