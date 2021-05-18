import os
from inspect import cleandoc

import discord
from discord.ext import commands
from dotenv import load_dotenv

import help_messages
from utils import CommonCog, check_allowed_channel, discord_processing, string_processing


load_dotenv()
token = os.getenv('API_AUTH_TOKEN')

class RSNLinkCommands(CommonCog, name='RSN Link Commands'):
    cog_check = check_allowed_channel

    @commands.command(aliases=["pair"], description=help_messages.link_help_msg)
    async def link(self, ctx, *, joinedName=None):
        if not joinedName:
            return await ctx.send("Please specify the RSN of the account you'd wish to link. !link <RSN>")

        if not string_processing.is_valid_rsn(joinedName):
            return await ctx.send(f"{joinedName} isn't a valid Runescape user name.")


        verifyID = await discord_processing.get_playerid_verification(self.bot.session, playerName=joinedName, token=token)

        if verifyID is None:
            embed = await installplugin_msg()
            return await ctx.send(embed=embed)

        previousAttempts = await discord_processing.get_player_verification_full_status(self.bot.session, playerName=joinedName, token=token)

        if len(previousAttempts) == 0:
            code = string_processing.id_generator()
        else:
            for status in previousAttempts:
                if int(status['Verified_status']) == 1:
                    isVerified = 1
                    break
            else:
                isVerified = 0

            if isVerified == 1:
                owner_verified_info = await discord_processing.get_verified_player_info(self.bot.session, playerName=joinedName, token=token)
                ownerID = owner_verified_info['Discord_id']
                if ownerID == ctx.author.id:
                    embed = await verified_msg(joinedName)
                    return await ctx.send(embed=embed)

            elif isVerified == 0:
                code = int(previousAttempts[len(previousAttempts) - 1]["Code"])


        await discord_processing.post_discord_player_info(self.bot.session, discord_id=ctx.author.id, player_id=verifyID, code=code, token=token)
        embed = await link_msg(joinedName=joinedName, code=code)
        await ctx.author.send(embed=embed)



    @commands.command(name="verify", description=help_messages.verify_help_msg)
    async def verify_comand(self, ctx, *, joinedName=None):
        if not joinedName:
            return await ctx.send("Please specify the RSN of the account you'd wish to view the verification status for. !verify <RSN>")

        if not string_processing.is_valid_rsn(joinedName):
            return await ctx.send(joinedName + " isn't a valid Runescape user name.")

        verifyStatus = await discord_processing.get_player_verification_full_status(self.bot.session, playerName=joinedName, token=token)

        try:
            for status in verifyStatus:
                if int(status['Verified_status']) == 1:
                    isVerified = True
                    break
            else:
                isVerified = False

            if isVerified:
                embed = await verified_msg(joinedName)
            else:
                embed = await unverified_msg(joinedName)
        except:
            embed = await unverified_msg(joinedName)

        await ctx.send(embed=embed)

    @commands.command(name="linked", aliases=["getlinks"], description=help_messages.linked_help_msg)
    async def linked_comand(self, ctx):
        linkedAccounts = await discord_processing.get_linked_accounts(self.bot.session, ctx.author.id, token)

        if len(linkedAccounts) == 0:
            await ctx.send("You do not have any OSRS accounts linked to this Discord ID. Use the !link command in order to link an account.")
        else:
            embed = discord.Embed(color=0x00ff00)

            names = "\n".join(acc['name'] for acc in linkedAccounts)
            embed.add_field (name="Linked Accounts:", value=f"{names}", inline=False)

            await ctx.author.send(embed=embed)


async def verified_msg(joinedName):
    embed = discord.Embed(title=f"{joinedName}'s Status:", color=0x00ff00)
    embed.add_field (name="Verified:", value=f"{joinedName} is Verified.", inline=False)
    embed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117238120-538b4f00-adfa-11eb-9c58-d5500af7d215.png")
    return embed


async def unverified_msg(joinedName):
    embed = discord.Embed(title=f"{joinedName}'s Status:", color=0xff0000)
    embed.add_field (name="Unverified:", value=f"{joinedName} is Unverified.", inline=False)
    embed.add_field (name="Next Steps:", value=f"Please type '!link {joinedName}'", inline=False)
    embed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117239076-19bb4800-adfc-11eb-94c4-27ff7e1217cc.png")
    return embed


async def installplugin_msg():
    embed = discord.Embed(title=f"User Not Found:", color=0xff0000)
    embed.add_field (name="Status:", value=f"No reports exist from specified player.", inline=False)
    embed.add_field (name="Next Steps:", value=f"Please install the Bot-Detector Plugin on RuneLite if you have not done so.\n\n" \
        + "If you have the plugin installed, you will need to disable Anonymous Reporting for us to be able to !link your account.", inline=False)
    embed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117361316-e1f9e200-ae87-11eb-840b-3bad75e80ff6.png")
    return embed


async def link_msg(joinedName, code) -> discord.Embed:
    embed = discord.Embed(title=f"Linking '{joinedName}':", color=0x0000ff)

    embed.add_field(name="STATUS", inline=False, value=cleandoc(f"""
            Request to link '{joinedName}'.
            "Access Code: {code}
        """)
    )
    embed.add_field(name="SETUP", inline=False, value=cleandoc(f"""
            Please read through these instructions.
            1. Open Old School Runescape through RuneLite.
            2. Login as: '{joinedName}'
            3. Join the clan channel: 'Ferrariic'.
            4. Verify that a Plugin Admin or Plugin Moderator is present in the channel.
            5. If a Plugin Admin or Plugin Moderator is not available, please leave a message in #bot-detector-commands.
            6. Type into the Clan Chat: '!Code {code}'.
            7. Type '!verify {joinedName}' in #bot-detector-commands channel to confirm that you have been Verified.
            8. Verification Process Complete.
        """)
    )
    embed.add_field(name="INFO", inline=False, value=cleandoc(f"""
            You may link multiple Runescape accounts via this method.
            1. If you change the name of your account(s) you must repeat this process with your new RSN(s).
            2. In the event of a name change please allow some time for your data to be transferred over.
        """)
    )
    embed.add_field(name="NOTICE", inline=False, value=cleandoc(f"""
            Do not delete this message.
            1. If this RSN was submitted in error, please type '!link <Your Correct RSN>'.
            2. This code will not expire, it is tied to your unique RSN:Discord Pair.
            3. If you are unable to become 'Verified' through this process, please contact an administrator for assistance.
        """)
    )

    return embed


def setup(bot):
    bot.add_cog(RSNLinkCommands(bot))
