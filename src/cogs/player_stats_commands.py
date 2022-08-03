import logging
import aiohttp

import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from src import config

logger = logging.getLogger(__name__)


class playerStatsCommands(Cog):
    def __init__(self, bot: discord.Client) -> None:
        """
        Initialize the playerStatsCommands class.
        :param bot: The discord bot client.
        """
        self.bot = bot

    def _batch(self, iterable, n=1) -> list:
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx : min(ndx + n, l)]

    @commands.command()
    async def lookup(self, ctx: Context, *, username):
        logger.debug(f"{ctx.author}, looking up: {username}")

        intro_msg = await ctx.send("Searching for User...")
        player = await config.api.get_player(username)

        if not player:
            await ctx.reply("Something went terribly wrong. :(")

        player_hiscore = await config.api.get_hiscore_latest(player.get("id"))

        if not player_hiscore:
            await ctx.reply("Could not find the user in our database")
        
        player_hiscore:dict = player_hiscore[0]
        ts = player_hiscore.get("timestamp")
        # _ = [logger.debug({k:v}) for k,v in player_hiscore.items()]

        # same structure as in osrs
        skills_list = [ 
            'Attack',           'Hitpoints',    'Mining',
            'Strength',         'Agility',      'Smithing',
            'Defence',          'Herblore',     'Fishing',
            'Ranged',           'Thieving',     'Cooking',
            'Prayer',           'Crafting',     'Firemaking',
            'Magic',            'Fletching',    'Woodcutting',
            'runecraft',        'Slayer',       'Farming',
            'Construction',     'Hunter',       'Total' 
        ]

        embeds, i = [], 0
        embed = discord.Embed(title=username, description="OSRS Hiscores Lookup", color=0x00ff00)
        embed.set_footer(text=f"Updated on: {ts}")
        for skill in skills_list:
            xp = player_hiscore.get(skill.lower())
            # logger.debug(f"{skill} - {xp}")
            embed.add_field(
                name=f"{skill}",
                value=f"EXP - {xp:,d}",
                inline=True
            )
        embeds.append(embed)

        exclude = ["id", "timestamp", "ts_date", "Player_id"]
        skills_list = [s.lower() for s in skills_list]
        bosses = [k for k in player_hiscore.keys() if k not in skills_list + exclude]
        embed = None

        # add the fields for the bosses
        for boss in bosses:

            if embed is None:
                embed = discord.Embed(title=username, description="OSRS Hiscores Lookup", color=0x00ff00)
                embed.set_footer(text=f"Updated on: {ts}")
            kc = player_hiscore.get(boss)
            
            # don't add empty kc
            if kc is None or kc <= 0:
                continue

            # logger.debug({boss:kc})
            embed.add_field(
                name=f"{boss}",
                value=f"KC - {kc:,d}",
                inline=True
            )

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
        await intro_msg.delete()