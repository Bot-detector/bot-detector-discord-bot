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

    @command(name="test", hidden=True)
    async def test_command(self, ctx):
        #mbed = await warn_msg()
        print(dir(ctx.guild))
        await ctx.guild.get_channel(825189024074563614).send("test")

    @command(name="updateallroles", hidden=True)
    @has_permissions(manage_roles=True)
    async def update_all_roles_command(self, ctx, spam):

        if spam is "spam":
            sendSpam = True
        else:
            sendSpam = False

        listUsers = await discord_processing.get_discords_ids_with_links(token)
        print(listUsers)

        for user in listUsers:
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

                if new_role is not current_role and sendSpam:
                    mbed = discord.Embed (
                            description = f"{member.display_name}, you are now a {new_role}!",
                            color = new_role.color
                        )

                    mbed.set_thumbnail(url="https://user-images.githubusercontent.com/45152844/116952387-8ac1fa80-ac58-11eb-8a31-5fe0fc6f5f88.gif")

                    await ctx.guild.get_channel(825189024074563614).send(embed=mbed)

                else:
                    pass
        
        return

async def warn_msg():
    mbed = discord.Embed(title=f"WARNING", color=0xff0000)
    mbed.add_field (name="= WARNING MESSAGE =", value="**Do not attempt to contact the Jmods or Admins in any channel regarding the status of your Runescape account: Doing so will result in an automatic permanent ban.**" + "\n" \
            + "**This is your only warning.**" + "\n", inline=False)
    mbed.set_image(url="https://user-images.githubusercontent.com/5789682/117366156-59327480-ae8e-11eb-8b08-6cf815d8a36e.png")
    return mbed


def setup(bot):
    bot.add_cog(ModCommands(bot))



