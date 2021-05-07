from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
import discord
import os

import utils.discord_processing as discord_processing
import utils.roles as roles

from dotenv import load_dotenv
load_dotenv()
token = os.getenv('API_AUTH_TOKEN')

class ModCommands(Cog, name='Moderator Commands'):

    def __init__(self, bot):
        self.bot = bot

    @command(name="warn", aliases=["youvedoneitnow"], hidden=True)
    async def warn_command(self, ctx):
        mbed = await warn_msg()
        await ctx.channel.send(embed=mbed)
        

    @command(name="updateallroles", hidden=True)
    @has_permissions(manage_roles=True)
    async def update_all_roles_command(self, ctx, spamChoice=""):

        if 'spam' in spamChoice:
            await ctx.channel.send(f"{ctx.author.mention} You are a monster. I won't do it!!")
        else:
            pass

        listUsers = await discord_processing.get_discords_ids_with_links(token)
        print(listUsers)

        for user in listUsers:
            try:
                member = await ctx.guild.fetch_member(user['Discord_id'])
                print(member)

                linkedAccounts = await discord_processing.get_linked_accounts(member.id, token)
                print(linkedAccounts)

                if(len(linkedAccounts) == 0):
                    #how the heck did we get here
                    pass
                else:
                    for r in member.roles:
                        if r.id == roles.special_roles["verified_rsn"]:
                            #awesome, you're verified.
                            break

                    else:
                        verified_role = discord.utils.find(lambda r: r.id == roles.special_roles["verified_rsn"], member.guild.roles)
                        await member.add_roles(verified_role)

                current_role = discord.utils.find(lambda r: 'Bot Hunter' in r.name, member.roles)
                new_role = await roles.get_bot_hunter_role(linkedAccounts, member)

                if(new_role == False):
                    pass
                else:
                    await roles.remove_old_roles(member)
                    await member.add_roles(new_role)
                    
            except Exception as e:
                    print(e)
        
        return

async def warn_msg():
    mbed = discord.Embed(title=f"WARNING", color=0xff0000)
    mbed.add_field (name="= WARNING MESSAGE =", value="**Do not attempt to contact the Jmods or Admins in any channel regarding the status of your Runescape account: Doing so will result in an automatic permanent ban.**" + "\n" \
            + "**This is your only warning.**" + "\n", inline=False)
    mbed.set_image(url="https://user-images.githubusercontent.com/5789682/117366156-59327480-ae8e-11eb-8b08-6cf815d8a36e.png")
    return mbed


def setup(bot):
    bot.add_cog(ModCommands(bot))



