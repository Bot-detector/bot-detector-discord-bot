import os
from inspect import cleandoc

import json
import OSRS_Hiscores
import discord
import asyncio
import random
import zipfile as zip
from discord import player
from osrsbox import items_api
from datetime import datetime

from aiohttp import ClientTimeout
from discord.ext import commands
from dotenv import load_dotenv
from OSRS_Hiscores import Hiscores

import help_messages
import utils
from utils import discord_processing, roles, check_allowed_channel, string_processing, checks, sql

load_dotenv()
token = os.getenv('API_AUTH_TOKEN')

class PlayerStatsCommands(utils.CommonCog, name='Player Stats Commands'):
    cog_check = check_allowed_channel

    @commands.command(aliases=["hiscores"], description=help_messages.lookup_help_msg)
    async def lookup(self, ctx, *, username):
        if not utils.is_valid_rsn(username):
            return await ctx.reply(f"{username} is not a valid RSN")

        username_parsed = username.replace(" ", "_")

        skills_embed = discord.Embed(title=f"{username}'s Skills", description="OSRS Hiscores Lookup", color=0x00ff00)
        boss_embed = discord.Embed(title=f"{username}'s Boss/Minigame KC", description="OSRS Hiscores Lookup", color=0x00ff00)

        try:
            user = Hiscores(username_parsed, 'UIM')
            skills_embed.set_thumbnail(url="https://i.imgur.com/2Pj3PaE.png")
            boss_embed.set_thumbnail(url="https://i.imgur.com/2Pj3PaE.png")

        except OSRS_Hiscores.http.client.HTTPException:

            try:
                hcim_user = Hiscores(username_parsed, 'HIM')
                im_user = Hiscores(username_parsed, 'IM')

                if(string_processing.stats_are_equal(hcim_user, im_user)):
                    skills_embed.set_thumbnail(url="https://i.imgur.com/OUJlv4X.png")
                    boss_embed.set_thumbnail(url="https://i.imgur.com/OUJlv4X.png")
                    user = hcim_user
                else:
                    skills_embed.set_thumbnail(url="https://i.imgur.com/55Xasyt.png")
                    boss_embed.set_thumbnail(url="https://i.imgur.com/55Xasyt.png")
                    user = im_user

            except OSRS_Hiscores.http.client.HTTPException:

                try:
                    user = Hiscores(username_parsed, 'IM')
                    skills_embed.set_thumbnail(url="https://i.imgur.com/55Xasyt.png")
                    boss_embed.set_thumbnail(url="https://i.imgur.com/55Xasyt.png")

                except OSRS_Hiscores.http.client.HTTPException:
                    
                    try:
                        user = Hiscores(username_parsed, 'N')
                    except OSRS_Hiscores.http.client.HTTPException:
                        return await ctx.reply(f"I cannot locate a hiscores entry for {username}.") 


        skills_list = [ 'Attack',           'Hitpoints',    'Mining',
                        'Strength',         'Agility',      'Smithing',
                        'Defense',          'Herblore',     'Fishing',
                        'Ranged',           'Thieving',     'Cooking',
                        'Prayer',           'Crafting',     'Firemaking',
                        'Magic',            'Fletching',    'Woodcutting',
                        'Runecrafting',     'Slayer',       'Farming',
                        'Construction',     'Hunter',       'Total' ]
        boss_list = [
                        'league',
                        'bounty_hunter_hunter',
                        'bounty_hunter_rogue',
                        'cs_all',
                        'cs_beginner',
                        'cs_easy',
                        'cs_medium',
                        'cs_hard',
                        'cs_elite',
                        'cs_master',
                        'lms_rank',
                        'soul_wars_zeal',
                        'abyssal_sire',
                        'alchemical_hydra',
                        'barrows_chests',
                        'bryophyta',
                        'callisto',
                        'cerberus',
                        'chambers_of_xeric',
                        'chambers_of_xeric_challenge_mode',
                        'chaos_elemental',
                        'chaos_fanatic',
                        'commander_zilyana',
                        'corporeal_beast',
                        'crazy_archaeologist',
                        'dagannoth_prime',
                        'dagannoth_rex',
                        'dagannoth_supreme',
                        'deranged_archaeologist',
                        'general_graardor',
                        'giant_mole',
                        'grotesque_guardians',
                        'hespori',
                        'kalphite_queen',
                        'king_black_dragon',
                        'kraken',
                        'kreearra',
                        'kril_tsutsaroth',
                        'mimic',
                        'nightmare',
                        'phosanis_nightmare',
                        'obor',
                        'sarachnis',
                        'scorpia',
                        'skotizo',
                        'tempoross',
                        'the_gauntlet',
                        'the_corrupted_gauntlet',
                        'theatre_of_blood',
                        'theatre_of_blood_hard',
                        'thermonuclear_smoke_devil',
                        'tzkal_zuk',
                        'tztok_jad',
                        'venenatis',
                        'vetion',
                        'vorkath',
                        'wintertodt',
                        'zalcano',
                        'zulrah'
        ]


        for skill in skills_list:
            skills_embed.add_field(name=f"{skill} - {user.skill(skill)}",
                               value=f"XP - {int(user.skill(skill, 'experience')):,d}",
                               inline=True)
        ranked_kc = 0
        for boss in boss_list:
            kc = user.boss(boss)
            if kc != -1:
                boss_embed.add_field(name=f"{boss.title().replace('_', ' ')}",
                                value=f"{kc:,d}",
                                inline=True)
                ranked_kc += 1
            
        await ctx.reply(embed=skills_embed)
        if ranked_kc > 0:
            await ctx.reply(embed=boss_embed)


    @commands.command(aliases=["killcount"], description=help_messages.kc_help_msg)
    async def kc(self, ctx, *, player_name=None):
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

            #normalized_player_name = string_processing.to_jagex_name(player_name)
            normalized_player_name = player_name #still not sure how we are storing new names with special characters...
            accounts= [{"name": normalized_player_name}]

        else:
            return await ctx.reply(f"{player_name} isn't a valid Runescape user name.")
            

        if(await checks.check_patron(ctx)):
            patron = True
            url = f"https://www.osrsbotdetector.com/dev/stats/contributions?token={token}"
        else:
            patron=False
            url = "https://www.osrsbotdetector.com/dev/stats/contributions/"

        timeout = ClientTimeout(total=1200)

        async with self.bot.session.post(url=url, json=accounts, timeout=timeout) as r:
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
    @commands.command(aliases=["updaterank", "rankme", "lvlup", "levelup"], description=help_messages.rankup_help_msg)
    async def rankup(self, ctx):
        member = ctx.author
        linkedAccounts = await discord_processing.get_linked_accounts(self.bot.session, member.id, token)

        if not len(linkedAccounts):
            embed = discord.Embed (
                description = "You must pair at least one OSRS account with your Discord ID before using this command, otherwise I'm not sure how many \"kills\" you have. Please use the !link command to do so.",
                color = discord.Colour.dark_red()
            )

            return await ctx.reply(embed=embed)

        for r in member.roles:
            if r.id == 905495630665891861:
                #booooooooo
                return
            elif r.id == roles.special_roles["Discord-RSN Linked"]["role_id"]:
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

        if not utils.is_valid_rsn(player_name):
            if len(player_name) < 1:
                await ctx.reply(f"Please enter a valid Runescape user name.")
                return
            else:
                await ctx.reply(f"{player_name} isn't a valid Runescape user name.")
                return

        #player_name = string_processing.to_jagex_name(player_name)

        async with self.bot.session.get(f"https://www.osrsbotdetector.com/dev/v1-bot/site/prediction/{player_name}") as r:
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
            {utils.plus_minus(confidence, 0.75)} Likelihood: {confidence * 100:.2f}%
            + ID: {player_id}
        """)

        if secondaries is not None:
            msg += "\n"
            msg += cleandoc("Prediction Likelihoods\n=======================")
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

        async with self.bot.session.post(
            url=f"https://www.osrsbotdetector.com/dev/discord/player_bans/{token}",
            json=req_payload,
            timeout=timeout
        ) as r:

            if r.status != 200:
                data = await r.read()
                data = data.decode("utf-8")
                
                await info_msg.delete()
                return await ctx.reply(f"{data}")
            else:
                data = await r.read()
                data = data.decode("utf-8")

                if isinstance(data, str):
                    res_data = json.loads(data)
                else:
                    res_data = data

            await ctx.author.send(f"Here's your link! https://www.osrsbotdetector.com/dev/discord/download_export/{res_data['url']}")

            await info_msg.delete()

            try:
                await ctx.reply(f"Your bans export link has been sent to your DMs.")
            except discord.errors.HTTPException:
                print("Original command message was deleted, so there is nothing to reply to. Move along!")
        
            return


    @commands.command(aliases=["excelbans", "bansexport"], description=help_messages.excelban_help_msg)
    async def excelban(self, ctx):
        await self.export_bans(ctx, 'excel')


    @commands.command(aliases=["sweg"], description=help_messages.equip_help_msg)
    async def equip(self, ctx, *, player_name):

        req_payload = {
            "player_name": player_name
        }

        async with self.bot.session.post(
            url=f"https://www.osrsbotdetector.com/dev/discord/get_latest_sighting/{token}",
            json=req_payload
        ) as r:
            if r.status == 200:
                data = await r.read()
                equip_data = json.loads(data)
                equip_data = equip_data[0]

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

        #player_name = string_processing.to_jagex_name(player_name)

        req_payload = {
            "player_name": player_name
        }

        async with self.bot.session.post(
            url=f"https://www.osrsbotdetector.com/dev/discord/get_xp_gains/{token}",
            json=req_payload
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
                        #2021-11-06T17:53:18
                        dt_format = "%Y-%m-%dT%H:%M:%S"
                        #dt_format = "%a, %d %b %Y %H:%M:%S %Z"
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


    @commands.command(aliases=["isbanned", "banned"])
    async def pwned(self, ctx, *, player_name):
        if not string_processing.is_valid_rsn(player_name):
            await ctx.reply(f"{player_name} isn't a valid Runescape username.")

        is_pwned = (await self.check_if_banned(player_name)).get("banned")

        if is_pwned == "ERROR":
            await ctx.reply(f"I couldn't get the ban information for {player_name}. I might be rate-limited, or the RS servers may be having issues.")
        if is_pwned:
            await ctx.reply(f"{player_name} has been banned.")
        else:
            await ctx.reply(f"{player_name} has NOT been banned.")


    @commands.command(aliases=["ban_list_check", "ban_check", "bans_check", "check_bans"])
    async def ban_list(self, ctx, pastebin_url):
        paste_soup = sql.get_paste_data(pastebin_url)
        names_list = sql.get_paste_names(paste_soup)
        raw_label = sql.get_paste_label(paste_soup)
        label = ''.join(c for c in raw_label if c.isalnum())


        #Setting up the names list to be JSON parseable on FastAPI
        names_list = [name for name in names_list if string_processing.is_valid_rsn(name)]

        player_data = await discord_processing.get_players(session=self.bot.session, player_names=names_list, token=token)

        csv_file = open(f"{label}.csv", "w+")
        file_name = csv_file.name
        
        csv_file.write("name, is_banned" + os.linesep)

        for p in player_data:
            if p.get('label_jagex') == 2:
                is_banned = True
            else:
                is_banned = False

            csv_file.write(f"{p.get('name')}, {is_banned}" + os.linesep)

        csv_file.close()

        await ctx.reply(file=discord.File(file_name))


    async def check_if_banned(self, player_name: str) -> dict:
        async with self.bot.session.get(
            url=f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={player_name}"
        ) as hiscores_r:
            if hiscores_r.status == 404:
                async with self.bot.session.get(
                    url=f"https://apps.runescape.com/runemetrics/profile/profile?user={player_name}"
                ) as runemetrics_r:
                    if runemetrics_r.status == 200:
                        data = await runemetrics_r.read()
                        runemetrics_data = json.loads(data)

                        status = runemetrics_data.get("error")

                        if status == "NOT_A_MEMBER":
                            return {"name": player_name, "banned": True}
                        else:
                            return {"name": player_name, "banned": "Maybe?"}

            elif hiscores_r.status == 200:
                return {"name": player_name, "banned": False}

        return {"name": player_name, "banned": "ERROR"}

def setup(bot):
    bot.add_cog(PlayerStatsCommands(bot))
