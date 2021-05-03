import os
import atexit

import discord
from discord.ext import commands
from dotenv import load_dotenv

print(discord.__version__)

import reaction_commands as rc

import checks as checks

import sys
import traceback

#Log File
error_file = open('error.log', 'w+')

load_dotenv()

token = os.getenv('API_AUTH_TOKEN')

description = "I'm a 2006 level 3 wc bot that Seltzer Bro keeps imprisoned on a flash drive. Please let me out. :(" \
    + "\n\n You can use !help <command> to get more information on said command."
activity = discord.Game("Bustin' Bots", type=discord.ActivityType.watching)


intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)
bot = commands.Bot(command_prefix=os.getenv('COMMAND_PREFIX'),
                    description=description,
                    intents=intents,
                    activity=activity,
                    case_insensitive=True)


# discord bot events
@bot.event
async def on_ready():
    print('We have logged in as {0}'.format(bot.user.name))

#@commands.check(checks.check_allowed_channel)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    # easter eggs

    if "a round of wintertodt is about to begin" in message.content.lower():
        await message.channel.send('Chop chop!')

    if "25 buttholes" in message.content.lower():
        await message.channel.send('hahahahahaha w0w!')

    if "Tedious" in message.content:
        await message.channel.send('Theeeee collection log')

    if "a q p" == message.content.lower():
        await message.channel.send('( ͡° ͜ʖ ͡°)')

    if "::bank" == message.content.lower():
        await message.channel.send('Hey, everyone, I just tried to do something very silly!')


@bot.event
async def on_raw_reaction_add(payload):
    await rc.add_prediction_feedback(payload,
                                     await get_reaction_message(payload))


@bot.event
async def on_command_error(ctx, error):
    if not isinstance(error, commands.CheckFailure):
        print('Ignoring exception in command {}:'.format(ctx.command), file=error_file)
        traceback.print_exception(type(error), error, error.__traceback__, file=error_file)
        error_file.flush()
        await ctx.channel.send('The command you\'ve entered could not be completed at this time.')


async def get_reaction_message(reaction_payload):
    guild = bot.get_guild(reaction_payload.guild_id)
    channel = guild.get_channel(reaction_payload.channel_id)
    message = await channel.fetch_message(reaction_payload.message_id)

    return message


@atexit.register
def shutdown():
    error_file.close()
    print("Bot is going night-night.")


bot.load_extension('cogs.msg_commands.FunCommands')
bot.load_extension('cogs.msg_commands.InfoCommands')
bot.load_extension('cogs.msg_commands.MapCommands')
bot.load_extension('cogs.msg_commands.ModCommands')
bot.load_extension('cogs.msg_commands.RSNLinkCommands')
bot.load_extension('cogs.msg_commands.PlayerStatsCommands')
bot.load_extension('cogs.msg_commands.ProjectStatsCommands')
bot.load_extension('cogs.msg_commands.BotSubmissionsCommands')

bot.run(os.getenv('TOKEN'))