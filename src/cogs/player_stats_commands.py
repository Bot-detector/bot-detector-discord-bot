import logging
from datetime import datetime
from inspect import cleandoc

import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from osrsbox import items_api
from src import config
from src.utils import string_processing
from src.utils.checks import PATREON_ROLE, VERIFIED_PLAYER_ROLE

logger = logging.getLogger(__name__)
ITEMS = items_api.load()

bot_hunter_roles = [
    {
        "role_id": 825165287526498314,
        "role_name": "Bot Hunter I",
        "min": 1,
        "max": 5,
    },  # 1 Ban
    {
        "role_id": 825165422721499167,
        "role_name": "Bot Hunter II",
        "min": 5,
        "max": 10,
    },  # 5 Bans
    {
        "role_id": 825165526262874133,
        "role_name": "Bot Hunter III",
        "min": 10,
        "max": 25,
    },  # 10 Ban
    {
        "role_id": 825169068667305995,
        "role_name": "Bot Hunter IV",
        "min": 25,
        "max": 50,
    },  # 25 Bans
    {
        "role_id": 825165991503069225,
        "role_name": "Bot Hunter V",
        "min": 50,
        "max": 100,
    },  # 50 Ban
    {
        "role_id": 825166170989658112,
        "role_name": "Bot Hunter VI",
        "min": 100,
        "max": 250,
    },  # 100 Bans
    {
        "role_id": 825166288321642507,
        "role_name": "Bot Hunter VII",
        "min": 250,
        "max": 500,
    },  # 250 Ban
    {
        "role_id": 825166386862489623,
        "role_name": "Bot Hunter VIII",
        "min": 500,
        "max": 1000,
    },  # 500 Bans
    {
        "role_id": 825166550947332136,
        "role_name": "Bot Hunter IX",
        "min": 1000,
        "max": 2500,
    },  # 1000 Ban
    {
        "role_id": 825166673337384990,
        "role_name": "Bot Hunter X",
        "min": 2500,
        "max": 5000,
    },  # 2500 Bans
    {
        "role_id": 825166781056286751,
        "role_name": "Bot Hunter XI",
        "min": 5000,
        "max": 10000,
    },  # 5000 Ban
    {
        "role_id": 825167037323673631,
        "role_name": "Bot Hunter XII",
        "min": 10000,
        "max": 25000,
    },  # 10000 Bans
    {
        "role_id": 825167642184777738,
        "role_name": "Bot Hunter XIII",
        "min": 25000,
        "max": 50000,
    },  # 25000 Ban
    {
        "role_id": 825167838753849384,
        "role_name": "Bot Hunter XIV",
        "min": 50000,
        "max": 100000,
    },  # 50000 Bans
    {
        "role_id": 825168089363644427,
        "role_name": "Bot Hunter XV",
        "min": 100000,
        "max": 250000,
    },  # 100000 Ban
    {
        "role_id": 825168309158281247,
        "role_name": "Bot Hunter XVI",
        "min": 250000,
        "max": 500000,
    },  # 250000 Bans
    {
        "role_id": 825168632615010371,
        "role_name": "Bot Hunter XVII",
        "min": 500000,
        "max": 750000,
    },  # 500000 Ban
    {
        "role_id": 825168881059758083,
        "role_name": "Bot Hunter XVIII",
        "min": 750000,
        "max": 1000000,
    },  # 750000 Bans
    {
        "role_id": 825169438835081216,
        "role_name": "Bot Hunter XIX",
        "min": 1000000,
        "max": 2000000,
    },  # 1000000 Ban
    {
        "role_id": 825169641491791902,
        "role_name": "Bot Hunter XX",
        "min": 2000000,
        "max": 100_000_000,
    },  # 2000000 Bans
]


class playerStatsCommands(Cog):
    def __init__(self, bot: discord.Client) -> None:
        """
        Initialize the playerStatsCommands class.
        :param bot: The discord bot client.
        """
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_any_role(VERIFIED_PLAYER_ROLE)  # verified
    async def lookup(self, ctx: Context, *, player_name):
        logger.debug(f"{ctx.author.name=}, {ctx.author.id=}, looking up: {player_name}")
        await ctx.typing()

        player = await config.api.get_player(player_name)

        if not player:
            await ctx.reply("Something went terribly wrong. :(")

        player_hiscore = await config.api.get_hiscore_latest(player.get("id"))

        if not player_hiscore:
            await ctx.reply("Could not find the user in our database")

        player_hiscore: dict = player_hiscore[0]
        ts = player_hiscore.get("timestamp")
        # _ = [logger.debug({k:v}) for k,v in player_hiscore.items()]

        # same structure as in osrs
        skills_list = [
            "Attack",
            "Hitpoints",
            "Mining",
            "Strength",
            "Agility",
            "Smithing",
            "Defence",
            "Herblore",
            "Fishing",
            "Ranged",
            "Thieving",
            "Cooking",
            "Prayer",
            "Crafting",
            "Firemaking",
            "Magic",
            "Fletching",
            "Woodcutting",
            "runecraft",
            "Slayer",
            "Farming",
            "Construction",
            "Hunter",
            "Total",
        ]

        embeds = []
        embed = discord.Embed(
            title=player_name, description="OSRS Hiscores Lookup", color=0x00FF00
        )
        embed.set_footer(text=f"Updated on: {ts}")
        for skill in skills_list:
            xp = player_hiscore.get(skill.lower())
            # logger.debug(f"{skill} - {xp}")
            embed.add_field(name=f"{skill}", value=f"EXP - {xp:,d}", inline=True)
        embeds.append(embed)

        exclude = ["id", "timestamp", "ts_date", "Player_id"]
        skills_list = [s.lower() for s in skills_list]
        bosses = [k for k in player_hiscore.keys() if k not in skills_list + exclude]
        embed = None

        # add the fields for the bosses
        for boss in bosses:

            if embed is None:
                embed = discord.Embed(
                    title=player_name,
                    description="OSRS Hiscores Lookup",
                    color=0x00FF00,
                )
                embed.set_footer(text=f"Updated on: {ts}")
            kc = player_hiscore.get(boss)

            # don't add empty kc
            if kc is None or kc <= 0:
                continue

            # logger.debug({boss:kc})
            embed.add_field(name=f"{boss}", value=f"KC - {kc:,d}", inline=True)

            # max 7 rows of 3 in an embed
            if len(embed.fields) >= 21:
                embeds.append(embed)
                embed = None

            # max 10 embeds per reply
            if len(embeds) >= 9:
                await ctx.reply(embeds=embeds)
                embeds = []

        if len(embed.fields) > 0:
            embeds.append(embed)

        if embeds != []:
            await ctx.reply(embeds=embeds)
        return

    @commands.hybrid_command()
    @commands.has_any_role(VERIFIED_PLAYER_ROLE)
    async def kc(self, ctx: Context):
        logger.debug(f"{ctx.author.name=}, {ctx.author.id=}, Requesting kc")
        await ctx.typing()

        linked_accounts = await config.api.get_discord_links(
            discord_id=str(ctx.author.id)
        )
        # logger.debug(f"{linked_accounts=}")

        if not linked_accounts:
            embed = discord.Embed(
                description=cleandoc(
                    f"""
                    Please use the !link command to pair an OSRS account.
                    You can use !verify to check if you are verified.
                """
                )
            )
            await ctx.reply(embed=embed)
            return

        linked_accounts = [
            {"name": acc.get("name")}
            for acc in linked_accounts
            if acc.get("Verified_status") == 1
        ]
        patreon = ctx.author.get_role(PATREON_ROLE)

        data = await config.api.get_contributions(
            players=linked_accounts, patreon=patreon
        )

        if not data:
            await ctx.reply("No data found, ")
            return

        manual_reports = int(data["manual"]["reports"])
        manual_bans = int(data["manual"]["bans"])
        manual_incorrect = int(data["manual"]["incorrect_reports"])

        total_reports = int(data["total"]["reports"])
        total_bans = int(data["total"]["bans"])
        total_possible_bans = int(data["total"]["possible_bans"])

        embed = discord.Embed(
            title=f"{linked_accounts[0].get('name')}'s Stats", color=0x00FF00
        )

        if manual_reports == 0:
            report_accuracy = None
        elif manual_incorrect == 0:
            report_accuracy = 100.00
        else:
            report_accuracy = round(
                (manual_bans / (manual_bans + manual_incorrect)) * 100, 2
            )

        embed.add_field(
            name="Reports Submitted:", value=f"{total_reports:,d}", inline=False
        )
        embed.add_field(
            name="Possible Bans:", value=f"{total_possible_bans:,d}", inline=False
        )
        embed.add_field(name="Confirmed Bans:", value=f"{total_bans:,d}", inline=False)

        if report_accuracy is not None:
            embed.add_field(
                name="Manual Flags:", value=f"{manual_reports:,d}", inline=False
            )
            embed.add_field(
                name="Manual Flag Accuracy:", value=f"{report_accuracy}%", inline=False
            )

        if patreon:
            total_xp_removed = int(data["total"]["total_xp_removed"])
            embed.add_field(
                name="Total exp removed:", value=f"{total_xp_removed:,d}", inline=False
            )

        embed.set_thumbnail(
            url="https://user-images.githubusercontent.com/5789682/117364618-212a3200-ae8c-11eb-8b42-9ef5e225930d.gif"
        )

        if total_reports == 0:
            embed.set_footer(
                text="If you have the plugin installed but are not seeing your KC increase\nyou may have to disable Anonymous Mode in your plugin settings.",
                icon_url="https://raw.githubusercontent.com/Bot-detector/bot-detector/master/src/main/resources/warning.png",
            )

        await ctx.reply(embed=embed)
        return

    @commands.hybrid_command()
    @commands.has_any_role(VERIFIED_PLAYER_ROLE)
    async def rankup(self, ctx: Context):
        logger.debug(f"{ctx.author.name=}, {ctx.author.id=}, Requesting rankup")
        await ctx.typing()

        linked_accounts = await config.api.get_discord_links(
            discord_id=str(ctx.author.id)
        )

        if not linked_accounts:
            embed = discord.Embed(
                description=cleandoc(
                    f"""
                    Please use the !link command to pair an OSRS account.
                    You can use !verify to check if you are verified.
                """
                )
            )
            await ctx.reply(embed=embed)
            return

        linked_accounts = [
            {"name": acc.get("name")}
            for acc in linked_accounts
            if acc.get("Verified_status") == 1
        ]
        data = await config.api.get_contributions(players=linked_accounts)
        bans = data["total"]["bans"]
        logger.debug(bans)

        # search until you find the role he should have
        role_dict = [r for r in bot_hunter_roles if r.get("max") > bans > r.get("min")]
        if not role_dict:
            embed = discord.Embed(
                description="You currently have no confirmed bans. Keep hunting those bots, and you'll be there in no time! :)",
                color=discord.Colour.dark_red(),
            )
            await ctx.reply(embed=embed)
            return

        role = role_dict[0]
        new_role = discord.utils.find(
            lambda r: r.id == role.get("role_id"), ctx.author.guild.roles
        )

        if ctx.author.get_role(role.get("role_id")):
            embed = discord.Embed(
                description=f"You are not yet eligible for a new role. Only **{role.get('max') - bans}** more confirmed bans and you'll be there! :D",
                color=new_role.color,
            )
            await ctx.reply(embed=embed)
            return

        # cleanup
        for r in ctx.author.roles:
            if "Bot Hunter" in r.name:
                await ctx.author.remove_roles(r, reason="rankup")

        await ctx.author.add_roles(new_role)
        embed = discord.Embed(
            description=f"{ctx.author.display_name}, you are now a {new_role}!",
            color=new_role.color,
        )
        embed.set_thumbnail(
            url="https://user-images.githubusercontent.com/45152844/116952387-8ac1fa80-ac58-11eb-8a31-5fe0fc6f5f88.gif"
        )
        await ctx.reply(embed=embed)
        return

    @commands.hybrid_command()
    async def predict(self, ctx: Context, *, player_name: str):
        logger.debug(f"{ctx.author.name=}, {ctx.author.id=}, Requesting predict")
        await ctx.typing()

        data = await config.api.get_prediction(player_name)

        if not data:
            await ctx.reply(f"I couldn't get a prediction for {player_name} :(")
            return

        name = data["player_name"]
        prediction = data["prediction_label"]
        confidence = data["prediction_confidence"]
        secondaries: dict = data["predictions_breakdown"]

        msg = cleandoc(
            f"""```diff
            + Name: {name}
            {string_processing.plus_minus(prediction, 'Real_Player')} Prediction: {prediction}
            {string_processing.plus_minus(confidence, 0.75)} Confidence: {float(confidence) * 100:.2f}%
            ============
            Prediction Breakdown
        """
        )

        msg += "\n"

        for key, value in secondaries.items():
            if value > 0:
                msg += cleandoc(
                    f"""
                    {string_processing.plus_minus(key, 'Real_Player')} {key}: {float(value) * 100:.2f}%
                """
                )

                msg += "\n"

        msg += "```"

        await ctx.reply(msg)
        return

    @commands.hybrid_command()
    @commands.has_any_role(VERIFIED_PLAYER_ROLE)
    async def pwned(self, ctx: Context, player_name: str):
        logger.debug(
            f"{ctx.author.name=}, {ctx.author.id=}, Requesting pwned: {player_name}"
        )
        player = await config.api.get_player(name=player_name)

        if not player:
            await ctx.reply(f"I couldn't get data for {player_name} :(")
            return

        if player.get("label_jagex") == 2:
            await ctx.reply(f"{player_name} has been banned")
        else:
            await ctx.reply(f"{player_name} has NOT been banned")
        return

    @commands.hybrid_command()
    @commands.has_any_role(VERIFIED_PLAYER_ROLE)
    async def gear(self, ctx: Context, player_name: str):
        logger.debug(
            f"{ctx.author.name=}, {ctx.author.id=}, Requesting gear: {player_name}"
        )
        sighting = await config.api.get_latest_sighting(name=player_name)

        if not sighting:
            await ctx.reply(f"I was unable to grab {player_name}'s latest outfit.")
            return

        embed = discord.Embed(
            title=f"{player_name}'s Last Seen Equipment",
            color=discord.Colour.dark_gold(),
        )

        equipped_items = 0

        for k, v in sighting[0].items():
            k: str
            v: int
            k = k.split("_")[1]
            k = k.capitalize()

            if v:
                try:
                    item_name = ITEMS.lookup_by_item_id(v).name
                except KeyError:
                    item_name = (
                        "Something currently unrecognizable. Perhaps a new item?"
                    )

                equipped_items += 1

                embed.add_field(name=k, value=item_name, inline=False)

        if equipped_items == 0:
            embed.add_field(
                name="(O_O;)",
                value=f"It appears that {player_name} was last seen.. naked.",
                inline=False,
            )
            embed.set_thumbnail(url="https://i.imgur.com/rYz39o6.png")
        await ctx.reply(embed=embed)
        return

    @commands.hybrid_command()
    @commands.has_any_role(VERIFIED_PLAYER_ROLE)
    async def xpgain(self, ctx: Context, player_name: str):
        logger.debug(
            f"{ctx.author.name=}, {ctx.author.id=}, Requesting xpgain: {player_name}"
        )

        gains = await config.api.get_xp_gainz(name=player_name)

        if not gains:
            await ctx.reply(f"I couldn't locate {player_name}'s hiscores gains. Sorry!")
            return

        embed = discord.Embed(
            title=f"{player_name}'s Last Seen Equipment",
            color=discord.Colour.dark_gold(),
        )

        gains: dict
        latest_data: dict = gains.get("latest")
        second_latest_data: dict = gains.get("second")

        embed = discord.Embed(
            title=f"{player_name}'s Latest Daily XP/KC Gains",
            color=discord.Colour.dark_gold(),
        )

        diffs = 0

        # TODO remove these from the API output
        keys_to_remove = ["id", "Player_id", "ts_date"]
        [latest_data.pop(key) for key in keys_to_remove]

        timestamp = latest_data.pop("timestamp")

        for k, v in latest_data.items():
            k = " ".join(k.split("_"))
            k = k.capitalize()

            if v is None:
                v = 0

            if v > 0:
                embed.add_field(name=k, value=f"{v:,d}", inline=True)
                diffs += 1

        if diffs == 0:
            await ctx.reply(
                f"It doesn't appear that {player_name} has trained anything recently. Slacker!"
            )

        else:
            if second_latest_data:
                # 2021-11-06T17:53:18
                dt_format = "%Y-%m-%dT%H:%M:%S"
                # dt_format = "%a, %d %b %Y %H:%M:%S %Z"
                latest_ts = datetime.strptime(timestamp, dt_format)
                second_latest_ts = datetime.strptime(
                    second_latest_data.pop("timestamp"), dt_format
                )
                timestamp_delta = latest_ts - second_latest_ts

                embed.add_field(
                    name="Duration", value=f"{timestamp_delta}", inline=False
                )
            else:
                embed.add_field(
                    name="Duration", value="Insufficient data", inline=False
                )

            embed.set_footer(text=f"Last Updated: {timestamp}")
            await ctx.reply(embed=embed)

        return
