import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import checks
import help_messages
import utils.discord_processing as discord_processing
import utils.string_processing as string_processing


load_dotenv()
token = os.getenv('API_AUTH_TOKEN')

class RSNLinkCommands(commands.Cog, name='RSN Link Commands'):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="link", aliases=["pair"], description=help_messages.link_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def link_command(self, ctx, *, joinedName=None):
        if not joinedName:
            return await ctx.send("Please specify the RSN of the account you'd wish to link. !link <RSN>")


        if not string_processing.is_valid_rsn(joinedName):
            await ctx.channel.send(joinedName  + " isn't a valid Runescape user name.")
            return

        verifyID = await discord_processing.get_playerid_verification(self.bot.session, playerName=joinedName, token=token)

        if verifyID is None:
            mbed = await installplugin_msg()
            return await ctx.send(embed=mbed)

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
                    mbed = await verified_msg(joinedName)
                    return await ctx.send(embed=mbed)

            elif isVerified == 0:
                code = int(previousAttempts[len(previousAttempts) - 1]["Code"])

        try:
            await discord_processing.post_discord_player_info(self.bot.session, discord_id=ctx.author.id, player_id=verifyID, code=code, token=token)
            mbed = await link_msg(joinedName=joinedName, code=code)
            await ctx.author.send(embed=mbed)
        except Exception as e:
            print(e)


    @commands.command(name="verify", description=help_messages.verify_help_msg)
    @commands.check(checks.check_allowed_channel)
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
                mbed = await verified_msg(joinedName)
            else:
                mbed = await unverified_msg(joinedName)
        except:
            mbed = await unverified_msg(joinedName)

        await ctx.send(embed=mbed)

    @commands.command(name="linked", aliases=["getlinks"], description=help_messages.linked_help_msg)
    @commands.check(checks.check_allowed_channel)
    async def linked_comand(self, ctx):
        linkedAccounts = await discord_processing.get_linked_accounts(self.bot.session, ctx.author.id, token)

        if len(linkedAccounts) == 0:
            await ctx.send("You do not have any OSRS accounts linked to this Discord ID. Use the !link command in order to link an account.")
        else:
            embed = discord.Embed(color=0x00ff00)

            names = "\n".join(acc['name'] for acc in linkedAccounts)
            embed.add_field (name="Linked Accounts:", value=f"{names}", inline=False)

            await ctx.author.send(embed=mbed)


async def verified_msg(joinedName):
    mbed = discord.Embed(title=f"{joinedName}'s Status:", color=0x00ff00)
    mbed.add_field (name="Verified:", value=f"{joinedName} is Verified.", inline=False)
    mbed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117238120-538b4f00-adfa-11eb-9c58-d5500af7d215.png")
    return mbed


async def unverified_msg(joinedName):
    mbed = discord.Embed(title=f"{joinedName}'s Status:", color=0xff0000)
    mbed.add_field (name="Unverified:", value=f"{joinedName} is Unverified.", inline=False)
    mbed.add_field (name="Next Steps:", value=f"Please type '!link {joinedName}'", inline=False)
    mbed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117239076-19bb4800-adfc-11eb-94c4-27ff7e1217cc.png")
    return mbed


async def installplugin_msg():
    mbed = discord.Embed(title=f"User Not Found:", color=0xff0000)
    mbed.add_field (name="Status:", value=f"No reports exist from specified player.", inline=False)
    mbed.add_field (name="Next Steps:", value=f"Please install the Bot-Detector Plugin on RuneLite if you have not done so.\n\n" \
        + "If you have the plugin installed, you will need to disable Anonymous Reporting for us to be able to !link your account.", inline=False)
    mbed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117361316-e1f9e200-ae87-11eb-840b-3bad75e80ff6.png")
    return mbed


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
            7. Type '!verify {joinedName}' in #bot-commands channel to confirm that you have been Verified.
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
