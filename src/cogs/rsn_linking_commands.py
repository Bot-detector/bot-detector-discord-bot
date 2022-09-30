import logging
from inspect import cleandoc

import discord
from discord.ext import commands
from discord.ext.commands import Context
from src import config
from src.utils import string_processing, checks

logger = logging.getLogger(__name__)


class rsnLinkingCommands(commands.Cog):
    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot
    
    def _batch(self, iterable, n=1) -> list:
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx : min(ndx + n, l)]

    async def verified_msg(self, name: str) -> discord.Embed:
        embed = discord.Embed(title=f"{name}'s Status:", color=0x00FF00)
        embed.add_field(name="Verified:", value=f"{name} is Verified.", inline=False)
        embed.set_thumbnail(
            url="https://user-images.githubusercontent.com/5789682/117238120-538b4f00-adfa-11eb-9c58-d5500af7d215.png"
        )
        return embed

    async def unverified_msg(self, name: str) -> discord.Embed:
        embed = discord.Embed(title=f"{name}'s Status:", color=0xFF0000)
        embed.add_field(
            name="Unverified:", value=f"{name} is Unverified.", inline=False
        )
        embed.add_field(
            name="Next Steps:", value=f"Please type '!link {name}'", inline=False
        )
        embed.set_thumbnail(
            url="https://user-images.githubusercontent.com/5789682/117239076-19bb4800-adfc-11eb-94c4-27ff7e1217cc.png"
        )
        return embed

    async def install_plugin_msg(self) -> discord.Embed:
        embed = discord.Embed(title=f"User Not Found:", color=0xFF0000)
        embed.add_field(
            name="Status:",
            value=f"No reports exist from specified player.",
            inline=False,
        )
        embed.add_field(
            name="Next Steps:",
            value=f"Please install the Bot-Detector Plugin on RuneLite if you have not done so.\n\nIf you have the plugin installed, you will need to disable Anonymous Reporting for us to be able to !link your account.",
            inline=False,
        )
        embed.set_thumbnail(
            url="https://user-images.githubusercontent.com/5789682/117361316-e1f9e200-ae87-11eb-840b-3bad75e80ff6.png"
        )
        return embed

    async def link_msg(self, name, code) -> discord.Embed:
        embed = discord.Embed(title=f"Linking '{name}':", color=0x0000FF)

        embed.add_field(
            name="STATUS",
            inline=False,
            value=cleandoc(
                f"""
                Request to link '{name}'.
                "Access Code: {code}
            """
            ),
        )
        embed.add_field(
            name="SETUP",
            inline=False,
            value=cleandoc(
                f"""
                Please read through these instructions.
                1. Open Old School Runescape through RuneLite.
                2. Login as: '{name}'
                3. Join the clan channel: 'Bot Detector'.
                4. Verify that a Plugin Admin or Plugin Moderator is present in the channel.
                5. If a Plugin Admin or Plugin Moderator is not available, please leave a message in #bot-detector-commands.
                6. Type into the Clan Chat: '!Code {code}'.
                7. Type '!verify {name}' in #bot-detector-commands channel to confirm that you have been Verified.
                8. Verification Process Complete.
            """
            ),
        )
        embed.add_field(
            name="INFO",
            inline=False,
            value=cleandoc(
                f"""
                You may link multiple Runescape accounts via this method.
                1. If you change the name of your account(s) you must repeat this process with your new RSN(s).
                2. In the event of a name change please allow some time for your data to be transferred over.
            """
            ),
        )
        embed.add_field(
            name="NOTICE",
            inline=False,
            value=cleandoc(
                f"""
                Do not delete this message.
                1. If this RSN was submitted in error, please type '!link <Your Correct RSN>'.
                2. This code will not expire, it is tied to your unique RSN:Discord Pair.
                3. If you are unable to become 'Verified' through this process, please contact an administrator for assistance.
            """
            ),
        )

        return embed

    @commands.hybrid_command(name="link")
    async def link(self, ctx: Context, *, name: str):
        logger.debug(f"{ctx.author.name=}, {ctx.author.id=}, Requesting link, {name=}")
        # check if a name is given
        if not name:
            await ctx.send(
                "Please specify the RSN of the account you'd wish to link. !link <RSN>"
            )
            return
        # check if the name is valid
        if not string_processing.is_valid_rsn(name):
            await ctx.send(f"{name} isn't a valid Runescape user name.")
            return

        # check if player exists on the bot detector api
        player = await config.api.get_player(name=name)
        if not player:
            embed = await self.install_plugin_msg()
            await ctx.send(embed=embed)
            return

        # get the db record for rsn & ctx.author.id
        linked_users = await config.api.get_discord_player(name)

        linked_user = [
            user for user in linked_users if user.get("Discord_id") == ctx.author.id
        ]

        if linked_user:
            linked_user = linked_user[0]
            linked_status = True if linked_user.get("Verified_status") == 1 else False
            if linked_status:
                embed = await self.verified_msg(name)
                await ctx.send(embed=embed)
                return
            else:
                code = linked_user.get("Code")
                # send user via pm the random code
                embed = await self.link_msg(name, code)
                await ctx.author.send(embed=embed)
                return

        # generate random code
        code = string_processing.get_random_id()

        # register verification
        await config.api.post_discord_code(
            discord_id=ctx.author.id, player_name=player.get("name"), code=code
        )

        # send user via pm the random code
        embed = await self.link_msg(name, code)
        await ctx.author.send(embed=embed)
        return

    @commands.hybrid_command(name="verify")
    async def verify(self, ctx: Context, name: str):
        logger.debug(
            f"{ctx.author.name=}, {ctx.author.id=}, Requesting verify, {name=}"
        )
        player = await config.api.get_player(name=name)
        if not player:
            embed = await self.install_plugin_msg()
            await ctx.reply(embed=embed)
            return

        # get the db record for rsn & ctx.author.id
        linked_users = await config.api.get_discord_player(name)

        if any(ctx.author.get_role(r) for r in checks.PREVILEGED_ROLES):
            linked_user = linked_users
        else:
            linked_user = [
                user for user in linked_users if user.get("Discord_id") == ctx.author.id
            ]

        if linked_user:
            linked_user = linked_user[0]
            linked_status = True if linked_user.get("Verified_status") == 1 else False
            if linked_status:
                embed = await self.verified_msg(name)
                verified_role = discord.utils.find(
                    lambda r: r.id == 831196988976529438, ctx.author.guild.roles
                )
                await ctx.author.add_roles(verified_role)
                await ctx.reply(embed=embed)
                return
            else:
                code = linked_user.get("Code")
                # send user via pm the random code
                embed = await self.link_msg(name, code)
                await ctx.author.send(embed=embed)
                return
        else:
            embed = await self.unverified_msg(name)
            await ctx.reply(embed=embed)
        return

    @commands.hybrid_command(name="linked")
    async def linked(self, ctx: Context):
        logger.debug(f"{ctx.author.name=}, {ctx.author.id=}, Requesting linked")
        links = await config.api.get_discord_links(ctx.author.id)

        if len(links) == 0:
            await ctx.send(
                "You do not have any OSRS accounts linked to this Discord ID. Use the !link command in order to link an account."
            )

        embeds = []
        for i, batch in enumerate(self._batch(links, n=21)):
            embed = discord.Embed(title="Linked Accounts",color=0x00FF00)
            for link in batch:
                link: dict
                if not link:
                    continue
                embed.add_field(name="a",value=link.get("name"), inline=True) # inline=False
            embeds.append(embed)

            # max 10 embeds per reply
            if i != 0 and i % 9 == 0:
                await ctx.reply(embeds=embeds)
                embeds = []

        # check if there are any embeds left
        if embeds != []:
            await ctx.reply(embeds=embeds)
        return
