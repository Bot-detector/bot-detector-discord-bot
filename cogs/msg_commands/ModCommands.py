import os

import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv

import utils.discord_processing as discord_processing
import utils.roles as roles


load_dotenv()
token = os.getenv("API_AUTH_TOKEN")

class ModCommands(commands.Cog, name="Moderator Commands"):
    def __init__(self, bot):
        self.bot = bot


    @commands.has_permissions(kick_members=True)
    @commands.command(name="warn", aliases=["youvedoneitnow"])
    async def warn_command(self, ctx):
        mbed = await warn_msg()
        await ctx.send(embed=mbed)

    @commands.has_role("Admin")
    @commands.command(name="updatefaq", hidden=True)
    async def updatefaq_command(self, ctx):
        channel = ctx.guild.get_channel(837497081987989516)
        await channel.purge(limit=100)

        url = "https://raw.githubusercontent.com/Bot-detector/bot-detector-discord-bot/main/FAQ.json"

        async with self.bot.session.get(url) as r:
            if r.status == 200:
                faqEntriesList = await r.json(content_type="text/plain; charset=utf-8")

        try:
            for entry in faqEntriesList:
                await channel.send(embed=self.generateEmbed(entry["embeds"][0]))
        except Exception as e:
            print(e)


    def generateEmbed(self, entry):
        embed = discord.Embed(
            title=entry["title"],
            color=discord.Color.gold()
        )

        fields = entry["fields"]
        for field in fields:
            embed.add_field(name=field["name"], value=field["value"], inline=False)

        return embed


    @commands.command(name="updateallroles", hidden=True)
    @commands.has_permissions(manage_roles=True)
    async def update_all_roles_command(self, ctx, spamChoice=""):

        if 'spam' in spamChoice:
            await ctx.channel.send(f"{ctx.author.mention} You are a monster. I won't do it!!")
        else:
            pass

        listUsers = await discord_processing.get_discords_ids_with_links(self.bot.session, token)

        for user in listUsers:
            try:
                member = await ctx.guild.fetch_member(user["Discord_id"])
                print(member)

                linkedAccounts = await discord_processing.get_linked_accounts(self.bot.session, member.id, token)

                if not len(linkedAccounts):
                    #how the heck did we get here
                    pass
                else:
                    for r in member.roles:
                        if r.id == roles.special_roles["Verified RSN"]["role_id"]:
                            #awesome, you're verified.
                            break

                    else:
                        verified_role = discord.utils.find(lambda r: r.id == roles.special_roles["Verified RSN"]["role_id"], member.guild.roles)
                        await member.add_roles(verified_role)

                role_info = await roles.get_bot_hunter_role(self.bot.session, linkedAccounts, member)

                print(role_info)

                if (isinstance(role_info, bool)):
                    pass
                elif (isinstance(role_info, tuple)):
                    await roles.remove_old_roles(member)
                    await member.add_roles(role_info[0])
                else:
                    await roles.remove_old_roles(member)
                    await member.add_roles(role_info)
            except Exception as d:
                print(d)
                pass


async def warn_msg():
    mbed = discord.Embed(title=f"WARNING", color=0xff0000)
    mbed.add_field (name="= WARNING MESSAGE =", value="**Do not attempt to contact the Jmods or Admins in any channel regarding the status of your Runescape account: Doing so will result in an automatic permanent ban.**" + "\n" \
            + "**This is your only warning.**" + "\n", inline=False)
    mbed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117366156-59327480-ae8e-11eb-8b08-6cf815d8a36e.png")
    return mbed


def setup(bot):
    bot.add_cog(ModCommands(bot))
