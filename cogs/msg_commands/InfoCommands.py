import datetime
from datetime import timezone

import discord
from discord.ext import commands

import help_messages
import utils
from utils import CommonCog, check_allowed_channel, roles


class InfoCommands(CommonCog, name='General Info Commands'):
    cog_check = check_allowed_channel

    @commands.command(description=help_messages.utc_help_msg)
    async def utc(self, ctx):
        await ctx.send(datetime.datetime.now(timezone.utc))

    @commands.command(description=help_messages.rules_help_msg)
    async def rules(self, ctx):
        await ctx.send('<#825137784112807946>')

    @commands.command(aliases=["site"], description=help_messages.website_help_msg)
    async def website(self, ctx):
        await ctx.send('https://www.osrsbotdetector.com/')

    @commands.command(description=help_messages.beta_help_msg)
    async def beta(self, ctx):
        await ctx.send('https://github.com/Bot-detector/bot-detector/wiki/Running-the-Development-Version-From-Source')

    @commands.command(description=help_messages.patreon_help_msg)
    async def patreon(self, ctx):
        await ctx.send('https://www.patreon.com/bot_detector')

    @commands.command(description=help_messages.github_help_msg)
    async def github(self, ctx):
        await ctx.send("https://github.com/Bot-detector")


    @commands.command(description=help_messages.invite_help_msg)
    async def invite(self, ctx):
        await ctx.send('https://discord.com/invite/JCAGpcjbfP')

    @commands.command(aliases=["issue"], description=help_messages.issues_help_msg)
    async def issues(self, ctx):
        await ctx.send('<#822851862016950282>')

    @commands.command(aliases=["ranks"], description=help_messages.roles_help_msg)
    async def roles(self, ctx):
        bot_mbed = discord.Embed(title=f"Bot Hunter Roles")

        for k, v in roles.bot_hunter_roles.items():
            bot_mbed.add_field(name=v["role_name"], value=f"Confirmed Bans: {k:,d}", inline=True)

        bot_mbed.add_field(name="Have enough for a new role?", value="Use `!rankup` in <#825189024074563614>", inline=False)
        special_roles_mbed = discord.Embed(title="Special Roles")

        for k, v in roles.special_roles.items():
            role_description = v["description"]
            special_roles_mbed.add_field(name=k, value=f"{role_description}", inline=False)

        await ctx.send(embed=bot_mbed)
        await ctx.send(embed=special_roles_mbed)

    @commands.command(aliases=["botlabels"], description=help_messages.labels_help_msg)
    async def labels(self, ctx):
        labels = await utils.get_player_labels(self.bot.session)

        labels_mbed = discord.Embed(title="Current Player Labels")

        for l in labels:
            labels_mbed.add_field(name=f"{l['label']}", value="\u200b", inline=True)

        labels_mbed.set_footer(text="Please note that some of these labels may not be avaiable yet in the current RuneLite Plugin Hub release.")

        await ctx.send(embed=labels_mbed)


def setup(bot):
    bot.add_cog(InfoCommands(bot))
