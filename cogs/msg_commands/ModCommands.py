import os
import time

import discord
from discord.errors import HTTPException
from discord.ext import commands
from dotenv import load_dotenv

from utils import CommonCog, discord_processing, roles

load_dotenv()
token = os.getenv("API_AUTH_TOKEN")

class ModCommands(CommonCog, name="Moderator Commands"):

    @commands.has_permissions(kick_members=True)
    @commands.command(aliases=["youvedoneitnow"])
    async def jmod(self, ctx):
        embed = await jmod_warn_msg()
        await ctx.send(embed=embed)


    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, limit):
        channel = ctx.guild.get_channel(ctx.channel.id)
        await channel.purge(limit = int(limit))


    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def give_link_roles(self, ctx):

        await ctx.reply("It begins...")

        num_updated = 0

        try:
            discord_ids = await discord_processing.get_discord_id_with_links(self.bot.session, token)

            for id_record in discord_ids:
                id = id_record.get('Discord_id')

                try:
                    member = await ctx.message.guild.fetch_member(id)

                    for r in member.roles:
                        if r.id == roles.special_roles["Discord-RSN Linked"]["role_id"]:
                            break

                    else:
                        verified_role = discord.utils.find(lambda r: r.id == roles.special_roles["Discord-RSN Linked"]["role_id"], member.guild.roles)
                        await member.add_roles(verified_role)
                        num_updated += 1

                except:
                    #The user isn't in our server anymore, or Discord just can't get them right now. Skip!
                    pass

                time.sleep(1)




        except HTTPException:
            await ctx.reply("I couldn't grab the list of Discord IDs.")


        await ctx.reply(f"The deed... is done. {num_updated} accounts now have the Discord-RSN Linked role.")


async def jmod_warn_msg():
    embed = discord.Embed(title="WARNING", color=0xff0000)
    embed.add_field (name="= WARNING MESSAGE =", value="**Do not attempt to contact the Jmods or Admins in any channel regarding the status of your Runescape account: Doing so will result in an automatic permanent ban.**" + "\n" \
            + "**This is your only warning.**" + "\n", inline=False)
    embed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117366156-59327480-ae8e-11eb-8b08-6cf815d8a36e.png")
    return embed


def setup(bot):
    bot.add_cog(ModCommands(bot))
