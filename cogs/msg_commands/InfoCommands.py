import datetime
from datetime import timezone

import discord
from discord.ext import commands

import checks
import help_messages
import utils.discord_processing as discord_processing
import utils.roles as roles


class InfoCommands(commands.Cog, name='General Info Commands'):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="utc", description=help_messages.utc_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def utc_time_command(self, ctx):
        await ctx.send(datetime.datetime.now(timezone.utc))

    @commands.command(name="rules", description=help_messages.rules_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def rules_command(self, ctx):
        await ctx.send('<#825137784112807946>')

    @commands.command(name="website", aliases=["site"], description=help_messages.website_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def website_command(self, ctx):
        await ctx.send('https://www.osrsbotdetector.com/')

    @commands.command(name="beta", description=help_messages.beta_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def beta_command(self, ctx):
        await ctx.send('https://github.com/Bot-detector/bot-detector/wiki/Running-the-Development-Version-From-Source')

    @commands.command(name="patreon", description=help_messages.patreon_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def patreon_command(self, ctx):
        await ctx.send('https://www.patreon.com/bot_detector')

    @commands.command(name="github", description=help_messages.github_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def github_command(self, ctx, repo):
        repos = {
            "core": "https://github.com/Bot-detector/Bot-Detector-Core-Files",
            "plugin": "https://github.com/Bot-detector/bot-detector",
            "discord": "https://github.com/Bot-detector/bot-detector-discord-bot",
            "website": "https://github.com/Bot-detector/Bot-Detector-Web"
        }

        not_found_text = f"{repo} isn't a valid GitHub repository name. Try 'Core' or 'Plugin'."
        repo_url = repos.get(repo.lower(), not_found_text)

        await ctx.send(repo_url)


    @commands.command(name="invite", description=help_messages.invite_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def invite_command(self, ctx):
        await ctx.send('https://discord.com/invite/JCAGpcjbfP')


    @commands.command(name="issues", aliases=["issue"], description=help_messages.issues_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def issues_command(self, ctx):
        await ctx.send('<#822851862016950282>')

    @commands.command(name="roles", aliases=["ranks"], description=help_messages.roles_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def roles_command(self, ctx):

        bot_mbed = discord.Embed(title=f"Bot Hunter Roles")

        for k, v in roles.bot_hunter_roles.items():
            bot_mbed.add_field(name=v["role_name"], value=f"Confirmed Bans: {k:,d}", inline=True)

        bot_mbed.add_field(name="Have enough for a new role?", value="Use `!rankup` in <#825189024074563614>", inline=False)

        special_roles_mbed = discord.Embed(title=f"Special Roles")

        for k, v in roles.special_roles.items():
            role_description = v["description"]
            special_roles_mbed.add_field(name=k, value=f"{role_description}", inline=False)

        await ctx.send(embed=bot_mbed)
        await ctx.send(embed=special_roles_mbed)

    @commands.command(name="labels", aliases=["botlabels"], description=help_messages.labels_help_msg)
    #@commands.check(checks.check_allowed_channel)
    async def labels_command(self, ctx):

        labels = await discord_processing.get_player_labels(self.bot.session)
        print(labels)

        labels_mbed = discord.Embed(title=f"Current Player Labels")

        for l in labels:
            labels_mbed.add_field(name=f"{l['label']}", value="\u200b", inline=True)

        labels_mbed.set_footer(text="Please note that some of these labels may not be avaiable yet in the current RuneLite Plugin Hub release.")

        await ctx.send(embed=labels_mbed)


def setup(bot):
    bot.add_cog(InfoCommands(bot))
