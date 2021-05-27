import asyncio
import os
import traceback
from inspect import cleandoc

import aiohttp
import discord
print(discord.__version__)
from discord.ext import commands
from dotenv import load_dotenv


# Load files
load_dotenv()


# Define constants
EASTER_EGGS = {
    "::bank": "Hey, everyone, I just tried to do something very silly!",
    "a round of wintertodt is about to begin": "Chop chop!",
    "25 buttholes": "hahahahahaha w0w!",
    "tedious": "Theeeee collection log",
    "a q p": "( ͡° ͜ʖ ͡°)",
    "ltt": "https://www.lttstore.com"
}


# Define bot
description = cleandoc("""
    I'm a 2006 level 3 wc bot that Seltzer Bro keeps imprisoned on a flash drive. Please let me out. :(
    You can use !help <command> to get more information on said command.
""")

activity = discord.Game("Bustin' Bots", type=discord.ActivityType.watching)
intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)
bot = commands.Bot(
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True),
    command_prefix=os.getenv('COMMAND_PREFIX'),
    description=description,
    case_insensitive=True,
    activity=activity,
    intents=intents
)


# Discord Bot events
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_connect():
    print("Bot connected successfully.")


@bot.event
async def on_disconnect():
    print("Bot disconnected.")


@bot.event
async def on_message(message):
    if message.author != bot.user:
        await bot.process_commands(message)

        # Easter eggs
        lowercase_msg = message.content.lower()
        for trigger in EASTER_EGGS:
            if trigger in lowercase_msg:
                await message.channel.send(EASTER_EGGS[trigger])


@bot.event
async def on_command_error(ctx, error):
    error = getattr(error, "original", error)

    if isinstance(error, (discord.Forbidden, commands.NoPrivateMessage)):
        await ctx.send("I couldn't send this information to you via direct message. Are your DMs enabled?")
    elif isinstance(error, (commands.CommandNotFound, commands.CheckFailure)):
        return
    else:
        print(f"Ignoring exception in command {ctx.command}:", file=bot.error_file)
        traceback.format_exception(type(error), error, error.__traceback__, file=bot.error_file)
        bot.error_file.flush()
        await ctx.send("The command you've entered could not be completed at this time.")
        await send_error_message(ctx, error)


async def send_error_message(ctx, error):
    error_embed = discord.Embed (
        title = "Discord Bot Encountered an Error",
        color = discord.Colour.dark_red()
    )

    error_embed.add_field(name="Author", value=f"{ctx.author}", inline=False)
    error_embed.add_field(name="Command", value=f"{ctx.invoked_with}", inline=False)
    error_embed.add_field(name="Message Link", value=f"https://discord.com/channels/{ctx.message.guild.id}/{ctx.message.channel.id}/{ctx.message.id}")
    error_embed.add_field(name="Error", value=f"{error}", inline=False)

    await bot.get_channel(847578925857112064).send(embed=error_embed)


# Recursively loads cogs from /cogs
for folder in os.listdir("cogs"):
    if os.path.isfile(f"cogs/{folder}") and folder.endswith(".py"):
        bot.load_extension(f"cogs.{folder[:-3]}")
        continue

    for cog_file in os.listdir(f"cogs/{folder}"):
        if cog_file.endswith(".py"):
            bot.load_extension(f"cogs.{folder}.{cog_file[:-3]}")


async def startup():
    async with aiohttp.ClientSession() as session:
        with open('error.log', 'w+') as error_file:
            bot.session = session
            bot.error_file = error_file
            bot.loop = asyncio.get_event_loop()

            await bot.start(os.getenv("TOKEN"))

    print("Bot is going night-night.")
    await bot.close()

asyncio.run(startup())
