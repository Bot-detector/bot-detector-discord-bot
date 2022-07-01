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
    async def link(self, ctx, *, joined_name=None):
        if not joined_name:
            return await ctx.send("Please specify the RSN of the account you'd wish to link. !link <RSN>")

        if not string_processing.is_valid_rsn(joined_name):
            return await ctx.send(f"{joined_name} isn't a valid Runescape user name.")

        #joined_name = string_processing.to_jagex_name(joined_name)

        previous_attempts = await discord_processing.get_verification_attempts(self.bot.session, player_name=joined_name, token=token)

        if len(previous_attempts) == 0:
            code = string_processing.id_generator()
            await discord_processing.post_discord_player_info(self.bot.session, discord_id=ctx.author.id, \
                player_name=joined_name, code=code, token=token)
            embed = await link_msg(joined_name=joined_name, code=code)
            await ctx.author.send(embed=embed)
        else:
            users_previous_attempt = {}
            user_previously_tried = False
            is_verified = False

            for attempt in previous_attempts:
                if attempt.get("Verified_status") == 1:
                    is_verified = True
                    break
                elif attempt.get("Discord_id") == ctx.author.id:
                    users_previous_attempt = attempt
                    user_previously_tried = True

            if is_verified:
                await ctx.reply(embed=await verified_msg(joined_name))
            elif user_previously_tried:
                code = users_previous_attempt.get('Code')
                embed = await link_msg(joined_name=joined_name, code=code)
                await ctx.author.send(embed=embed)
            else:
                code = string_processing.id_generator()
                await discord_processing.post_discord_player_info(self.bot.session, discord_id=ctx.author.id, \
                    player_name=joined_name, code=code, token=token)
                embed = await link_msg(joined_name=joined_name, code=code)
                await ctx.author.send(embed=embed)

        return


    @commands.command(name="verify", description=help_messages.verify_help_msg)
    async def verify_comand(self, ctx, *, joined_name=None):
        if not joined_name:
            return await ctx.send("Please specify the RSN of the account you'd wish to view the verification status for. !verify <RSN>")

        if not string_processing.is_valid_rsn(joined_name):
            return await ctx.send(joined_name + " isn't a valid Runescape user name.")

        joined_name = string_processing.to_jagex_name(joined_name)

        verifyStatus = await discord_processing.get_player_verification_full_status(self.bot.session, player_name=joined_name, token=token)

        try:
            for status in verifyStatus:
                if int(status['Verified_status']) == 1:
                    isVerified = True
                    break
            else:
                isVerified = False

            if isVerified:
                embed = await verified_msg(joined_name)
            else:
                embed = await unverified_msg(joined_name)
        except:
            embed = await unverified_msg(joined_name)

        await ctx.send(embed=embed)


    @commands.command(name="linked", aliases=["getlinks"], description=help_messages.linked_help_msg)
    async def linked_comand(self, ctx):
        linked_accounts = await discord_processing.get_linked_accounts(self.bot.session, ctx.author.id, token)

        if len(linked_accounts) == 0:
            await ctx.send("You do not have any OSRS accounts linked to this Discord ID. Use the !link command in order to link an account.")
        else:
            embed = discord.Embed(color=0x00ff00)

            names = "\n".join(acc['name'] for acc in linked_accounts)
            embed.add_field (name="Linked Accounts:", value=f"{names}", inline=False)

            await ctx.author.send(embed=embed)


async def verified_msg(joined_name):
    embed = discord.Embed(title=f"{joined_name}'s Status:", color=0x00ff00)
    embed.add_field (name="Verified:", value=f"{joined_name} is Verified.", inline=False)
    embed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117238120-538b4f00-adfa-11eb-9c58-d5500af7d215.png")
    return embed


async def unverified_msg(joined_name):
    embed = discord.Embed(title=f"{joined_name}'s Status:", color=0xff0000)
    embed.add_field (name="Unverified:", value=f"{joined_name} is Unverified.", inline=False)
    embed.add_field (name="Next Steps:", value=f"Please type `!link {joined_name}`. If you have already done so, please check your DMs for instructions on how to complete your verification.", inline=False)
    embed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117239076-19bb4800-adfc-11eb-94c4-27ff7e1217cc.png")
    return embed


async def installplugin_msg():
    embed = discord.Embed(title=f"User Not Found:", color=0xff0000)
    embed.add_field (name="Status:", value=f"No reports exist from specified player.", inline=False)
    embed.add_field (name="Next Steps:", value=f"Please install the Bot-Detector Plugin on RuneLite if you have not done so.\n\n" \
        + "If you have the plugin installed, you will need to disable Anonymous Uploading for us to be able to !link your account.", inline=False)
    embed.set_thumbnail(url="https://user-images.githubusercontent.com/5789682/117361316-e1f9e200-ae87-11eb-840b-3bad75e80ff6.png")
    return embed


async def link_msg(joined_name, code) -> discord.Embed:
    embed = discord.Embed(title=f"Linking '{joined_name}':", color=0x0000ff)

    embed.add_field(name="STATUS", inline=False, value=cleandoc(f"""
            **Request to Link:** `{joined_name}`.
            **Access Code:** `{code}`
        """)
    )
    embed.add_field(name="SETUP", inline=False, value=cleandoc(f"""
            **Please read through these instructions.**

            1. Open Old School Runescape through RuneLite.

            2. Login as: `{joined_name}`

            3. Join the following clan chat: `Bot Detector`

            4. Verify that a Plugin Admin or Plugin Moderator is present in the channel. See <#856983841825620018> for the list of admin/mod ranks to look for.

            5. If a Plugin Admin or Plugin Moderator is not available, please leave a message in <#825189024074563614>

            6. Type into the Clan Chat: `!Code {code}`. It must match this exact pattern so that our clients can detect it properly.

            7. To confirm that your verification is complete type `!verify {joined_name}` in <#825189024074563614>
            
            8. If this is your first time linking, consider also using `!rankup` to obtain the `Verified` role, as well as any kc role you may be eligible for.

            9. You may now use the `!excelban` command to receive an export of the bans you have contributed to. You also no longer need to
            specify a name whenever using the `!kc` command if you are trying to view your own "killcount".

        """)
    )
    embed.add_field(name="INFO", inline=False, value=cleandoc(f"""
            **You may link multiple Runescape accounts via this method.**

            1. If you change the name of your account(s) you must repeat this process with your new RSN(s).

            2. In the event of a name change, you may ask for a kc transfer after linking your new RSN by opening a ticket in <#920169469039485028>. If we can confirm you were verified on both names, we'll transfer your stats over.

            3. If you use the plugin on multiple accounts and you have them linked, using the `!kc` command will show you your combined total. You will also see the ban breakdowns for all of your accounts in your `!excelban` export.

        """)
    )
    embed.add_field(name="NOTICE", inline=False, value=cleandoc(f"""
            **Do not delete this message.**

            1. If this RSN was submitted in error, please type '!link <Your Correct RSN>'.

            2. This code will not expire, it is tied to your unique RSN:Discord Pair.

            3. If you are unable to become 'Verified' through this process, please contact an administrator for assistance.
        """)
    )

    return embed


def setup(bot):
    bot.add_cog(RSNLinkCommands(bot))
