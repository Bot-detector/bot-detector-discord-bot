import os
from inspect import cleandoc

import json
import discord
import zipfile as zip
from osrsbox import items_api
from datetime import datetime

from aiohttp import ClientTimeout
from discord.ext import commands
from dotenv import load_dotenv
from OSRS_Hiscores import Hiscores

import help_messages
import utils
from utils import discord_processing, roles, check_allowed_channel, string_processing, checks

load_dotenv()
token = os.getenv('API_AUTH_TOKEN')

class PlayerStatsCommands(utils.CommonCog, name='Player Stats Commands'):
    cog_check = check_allowed_channel

    @commands.command(aliases=["hiscores"], description=help_messages.lookup_help_msg)
    async def lookup(self, ctx, *, username):
        if not utils.is_valid_rsn(username):
            return await ctx.reply(f"{username} is not a valid RSN")

        try:
            username_parsed = username.replace(" ", "_")
            intro_msg = await ctx.reply("Searching for User... If there is no response, there was no account found.")
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

            await ctx.reply(embed=embed)

        except Exception as e:
            await ctx.reply("Something went terribly wrong. :(")
            raise e

        await intro_msg.delete()


    @commands.command(aliases=["killcount"], description=help_messages.kc_help_msg)
    async def kc(self, ctx, *, player_name=None):
        await ctx.trigger_typing()
        if not player_name:
            accounts = await discord_processing.get_linked_accounts(self.bot.session, ctx.author.id, token)

            if not accounts:
                embed = discord.Embed(
                    description=cleandoc(f"""
                        It doesn't look like you have any OSRS accounts linked to your Discord ID.\n\n
                        Please specify an OSRS username (ex: `!kc Seltzer Bro`) or use `!link YourRSN` to link an OSRS account to your Discord account. Once you have at least one account linked the `!kc` command will automatically know to pull your own "killcount".
                        You *do not* need to link an account before using this command.

                        You can `!link` multiple accounts to get your combined "killcount" if you use the plugin on multiple accounts.

                        For more information type `!help link`
                    """)
                )

                return await ctx.reply(embed=embed)

            embed = discord.Embed(title=f"{ctx.author.display_name}'s Stats", color=0x00ff00)

        elif utils.is_valid_rsn(player_name):

            embed = discord.Embed(title=f"{player_name}'s Stats", color=0x00ff00)

            normalized_player_name = string_processing.to_jagex_name(player_name)
            accounts= [{"name": normalized_player_name}]

        else:
            return await ctx.reply(f"{player_name} isn't a valid Runescape user name.")
            

        if(await checks.check_patron(ctx)):
            patron = True
            url = f"https://bigboi.osrsbotdetector.com/stats/contributionsplus/{token}"
        else:
            patron=False
            url = "https://bigboi.osrsbotdetector.com/stats/contributions/"


        async with self.bot.session.get(url=url, json=json.dumps(accounts)) as r:
            if r.status != 200:
                return await ctx.reply(f"Couldn't grab the !kc for {ctx.author.display_name}")
            js = await r.json()


        embed = await self.assemble_kc_embed(embed=embed, js=js, is_patron=patron)

        await ctx.reply(embed=embed)


    async def assemble_kc_embed(self, embed: discord.Embed, js: dict, is_patron: bool):

        manual_reports = js['manual']['reports']
        manual_bans = js['manual']['bans']
        manual_incorrect = js['manual']['incorrect_reports']
        total_reports = js['total']['reports']
        total_bans = js['total']['bans']
        total_possible_bans = js['total']['possible_bans']
        feedback = js['total']['feedback']
     
        if manual_bans == 0:
            report_accuracy = None
        elif manual_incorrect == 0:
            report_accuracy = 100.00
        else:
            report_accuracy = round((manual_bans / (manual_bans + manual_incorrect)) * 100, 2)

        embed.add_field(name="Sightings Submitted:", value=f"{total_reports:,d}", inline=False)
        embed.add_field(name="Possible Bans:", value=f"{total_possible_bans:,d}", inline=False)
        embed.add_field(name="Confirmed Bans:", value=f"{total_bans:,d}", inline=False)

        if report_accuracy is not None:
            embed.add_field(name="Manual Flags:", value=f"{manual_reports:,d}", inline=False)
            embed.add_field(name="Manual Flag Accuracy:", value=f"{report_accuracy}%", inline=False)

        if feedback > 0:
            embed.add_field(name="Feedback Submitted:", value=f"{feedback:,d}", inline=False)

        if(is_patron):
            embed.add_field(name="Total XP Removed:", value=f"{js['total']['total_xp_removed']:,.0f}", inline=False)

        embed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117364618-212a3200-ae8c-11eb-8b42-9ef5e225930d.gif")

        if total_reports == 0:
            embed.set_footer(text="If you have the plugin installed but are not seeing your KC increase\nyou may have to disable Anonymous Uploading in your plugin settings.",
            icon_url="https://raw.githubusercontent.com/Bot-detector/bot-detector/master/src/main/resources/warning.png")

        return embed


    #rank up '/discord/get_linked_accounts/<token>/<discord_id>
    @commands.command(aliases=["updaterank", "rankme"], description=help_messages.rankup_help_msg)
    async def rankup(self, ctx):
        await ctx.trigger_typing()
        member = ctx.author
        linkedAccounts = await discord_processing.get_linked_accounts(self.bot.session, member.id, token)

        if not len(linkedAccounts):
            embed = discord.Embed (
                description = "You must pair at least one OSRS account with your Discord ID before using this command, otherwise I'm not sure how many \"kills\" you have. Please use the !link command to do so.",
                color = discord.Colour.dark_red()
            )

            return await ctx.reply(embed=embed)

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

            return await ctx.reply(embed=embed)

        await roles.remove_old_roles(member)
        await member.add_roles(new_role)

        if new_role == current_role:
            embed = discord.Embed(
                    description = f"You are not yet eligible for a new role. Only **{next_role_amount - current_amount}** more confirmed bans and you'll be there! :D",
                    color = new_role.color
            )

            return await ctx.reply(embed=embed)

        embed = discord.Embed(
            description=f"{ctx.author.display_name}, you are now a {new_role}!",
            color=new_role.color
        )

        embed.set_thumbnail(url="https://user-images.githubusercontent.com/45152844/116952387-8ac1fa80-ac58-11eb-8a31-5fe0fc6f5f88.gif")
        await ctx.reply(embed=embed)


    @commands.command(aliases=["detect"], description=help_messages.predict_help_msg)
    async def predict(self, ctx, *, player_name):

        pending_msg = await ctx.reply("Searching the database for the predicted username.")
        await ctx.trigger_typing()

        if not utils.is_valid_rsn(player_name):
            if len(player_name) < 1:
                await ctx.reply(f"Please enter a valid Runescape user name.")
                return
            else:
                await ctx.reply(f"{player_name} isn't a valid Runescape user name.")
                return

        player_name = string_processing.to_jagex_name(player_name)

        async with self.bot.session.get(f"https://www.osrsbotdetector.com/api/site/prediction/{player_name}") as r:
            if r.status != 200:
                return await ctx.reply(f"I couldn't get a prediction for {player_name} :(")

            js = await r.json()

        name =        js.get("player_name")
        prediction =  js.get("prediction_label")
        player_id =   js.get("player_id")
        confidence =  js.get("prediction_confidence")
        secondaries = js.get("secondary_predictions")

        msg = cleandoc(f"""```diff
            + Name: {name}
            {utils.plus_minus(prediction, 'Real_Player')} Prediction: {prediction}
            {utils.plus_minus(confidence, 0.75)} Confidence: {confidence * 100:.2f}%
            + ID: {player_id}
        """)

        if secondaries is not None:
            msg += "\n"
            msg += cleandoc("Prediction Breakdown\n=======================")
            msg += "\n"

            for predict in secondaries:
                msg += cleandoc(f"""
                    {utils.plus_minus(predict[0], 'Real_Player')} {predict[0]}: {predict[1] * 100:.2f}%
                """)

                msg += "\n"

        msg += "```"

        await pending_msg.delete()
        await ctx.reply(msg)

        #TODO Add back in the feedback reactions. Right now I can only get the first one added to load.

    async def export_bans(self, ctx, file_type):
        discord_id = ctx.author.id
        display_name = ctx.author.display_name

        req_payload = {
            "discord_id": discord_id,
            "display_name": display_name,
            "file_type": file_type
        }

        info_embed = discord.Embed(
                    description = "I'm going to try to get that ready for you, and if it works I'll DM you a download link. This command is currently under maintenance and may fail."
        )

        info_embed.set_thumbnail(url="https://i.pinimg.com/originals/c1/b4/ee/c1b4ee02fc804310213be0ca427af5f8.png")

        info_msg = await ctx.reply(embed=info_embed)

        #temporary until task queue is up in fastapi
        timeout = ClientTimeout(total=1200)

        async with self.bot.session.get(
            url=f"https://bigboi.osrsbotdetector.com/discord/player_bans/{token}",
            json=json.dumps(req_payload),
            timeout=timeout
        ) as r:

            if r.status != 200:
                data = await r.read()
                data = data.decode("utf-8")

                res_data = json.loads(data)
                
                await info_msg.delete()
                return await ctx.reply(f"{res_data['error']}")
            else:
                data = await r.read()
                data = data.decode("utf-8")

                if isinstance(data, str):
                    res_data = json.loads(data)
                else:
                    res_data = data

            await ctx.author.send(f"Here's your link! https://bigboi.osrsbotdetector.com/discord/download_export/{res_data['url']}")

            await info_msg.delete()

            try:
                await ctx.reply(f"Your bans export link has been sent to your DMs.")
            except discord.errors.HTTPException:
                print("Original command message was deleted, so there is nothing to reply to. Move along!")
        
            return


    @commands.command(aliases=["excelbans", "bansexport"], description=help_messages.excelban_help_msg)
    async def excelban(self, ctx):
        await self.export_bans(ctx, 'excel')


    @commands.command(aliases=["csvbans"], description=help_messages.csvban_help_msg)
    async def csvban(self, ctx):
        await self.export_bans(ctx, 'csv')


    @commands.command(aliases=["sweg"], description=help_messages.equip_help_msg)
    async def equip(self, ctx, *, player_name):

        player_name = string_processing.to_jagex_name(player_name)

        req_payload = {
            "player_name": player_name
        }

        async with self.bot.session.get(
            url=f"https://www.osrsbotdetector.com/api/discord/get_latest_sighting/{token}",
            json=json.dumps(req_payload)
        ) as r:
            if r.status == 200:
                data = await r.read()
                equip_data = json.loads(data)

                embed = discord.Embed(
                        title = f"{player_name}'s Last Seen Equipment",
                        color = discord.Colour.dark_gold()
                    )

                items = items_api.load()

                equipped_items = 0
                
                for k,v in equip_data.items():
                    k = k.split("_")[1]
                    k = k.capitalize()

                    if v:
                        try:
                            item_name = items.lookup_by_item_id(v).name
                        except KeyError:
                            item_name = "Something currently unrecognizable. Perhaps a new item?"

                        v = item_name #TODO Add image here as well
                        equipped_items += 1

                        embed.add_field(name=k, value=v, inline=False)

                if equipped_items == 0:
                    embed.add_field(name="(O_O;)", value=f"It appears that {player_name} was last seen.. naked.", inline=False)
                    embed.set_thumbnail(url="https://i.imgur.com/rYz39o6.png")
                    
                await ctx.reply(embed=embed)

            else:
                await ctx.reply(f"I was unable to grab {player_name}'s latest outfit.")


    @commands.command(aliases=["gainz", "xpdiff", "xpgains", "gains"], description=help_messages.xpgain_help_msg)
    async def xpgain(self, ctx, *, player_name):

        player_name = string_processing.to_jagex_name(player_name)

        req_payload = {
            "player_name": player_name
        }

        async with self.bot.session.get(
            url=f"https://www.osrsbotdetector.com/api/discord/get_xp_gains/{token}",
            json=json.dumps(req_payload)
        ) as r:
            if r.status == 200:
                data = await r.read()
                gains_data = json.loads(data)

                latest_data = gains_data.get("latest")
                second_latest_data = gains_data.get("second")

                embed = discord.Embed(
                        title = f"{player_name}'s Latest Daily XP/KC Gains",
                        color = discord.Colour.dark_gold()
                    )

                diffs = 0

                #TODO remove these from the API output
                keys_to_remove = ["id", "Player_id", "ts_date"]
                [latest_data.pop(key) for key in keys_to_remove]
                
                timestamp = latest_data.pop("timestamp")
                
                for k,v in latest_data.items():
                    k = " ".join(k.split("_"))
                    k = k.capitalize()

                    if v > 0:
                        embed.add_field(name=k, value=f"{v:,d}", inline=True)
                        diffs += 1

                if diffs == 0:
                    await ctx.reply(f"It doesn't appear that {player_name} has trained anything recently. Slacker!")

                else:
                    if second_latest_data:
                        dt_format = "%a, %d %b %Y %H:%M:%S %Z"
                        latest_ts = datetime.strptime(timestamp, dt_format)
                        second_latest_ts = datetime.strptime(second_latest_data.pop("timestamp"), dt_format)
                        timestamp_delta = latest_ts - second_latest_ts
                        
                        embed.add_field(name="Duration", value=f"{timestamp_delta}", inline=False)
                    else:
                        embed.add_field(name="Duration", value="Insufficient data", inline=False)

                    embed.set_footer(text=f"Last Updated: {timestamp}")
                    await ctx.reply(embed=embed)

            else:
                await ctx.reply(f"I couldn't locate {player_name}'s hiscores gains. Sorry!")


def setup(bot):
    bot.add_cog(PlayerStatsCommands(bot))
