import os
import asyncio
import datetime
import json
import uvloop
import traceback
from inspect import cleandoc
from json import JSONDecodeError
from typing import List

import aiohttp
import discord
print(discord.__version__)
from discord.ext import commands, tasks
from dotenv import load_dotenv
from utils import roles, string_processing
from utils.discord_processing import get_latest_feedback, get_player


# Load files
load_dotenv()


# Define constants
EASTER_EGGS = {
    "::bank": "Hey, everyone, I just tried to do something very silly!",
    "a round of wintertodt is about to begin": "Chop chop!",
    "25 buttholes": "hahahahahaha w0w!",
    "a q p": "( ͡° ͜ʖ ͡°)",
}

banned_clients = [
    "openosrs",
    "bluelite",
    "runeliteplus",
    "run-elite",
    "meteorlite"
]

# Define bot
description = cleandoc("""
    I'm a 2006 level 3 wc bot that Seltzer Bro keeps imprisoned on a flash drive. Please let me out. :(
    You can use !help <command> to get more information on said command.
""")

activity = discord.Game("Bustin' Bots", type=discord.ActivityType.watching)
intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True, presences=True)
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
async def on_member_update(before: discord.Member, after: discord.Member):
    try:
        if(after.activity.name.lower() in banned_clients):
            await roles.add_banned_client_role(after)

    except AttributeError:
        #no activity
        pass


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

    if isinstance(error, (commands.NoPrivateMessage)):
        await ctx.send("I couldn't send this information to you via direct message. Are your DMs enabled?")
    elif isinstance(error, (discord.Forbidden)):
        await ctx.send("Discord is forbidding me from sending the message you've requested. Sorry!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"You missed the argument `{error.param.name}` for this command!")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(f"I can't understand this command message! Please check `!help {ctx.command}`")
    elif isinstance(error, (commands.CommandNotFound, commands.CheckFailure)):
        return
    else:
        error_traceback = traceback.format_exception(type(error), error, error.__traceback__)
        print(f"Ignoring exception in command {ctx.command}:\n", *error_traceback, file=bot.error_file)
        bot.error_file.flush()

        await asyncio.gather(
            send_error_message(ctx, error, error_traceback),
            ctx.send("The command you've entered could not be completed at this time.")
        )


#Recurring Tasks
@tasks.loop(minutes=5, count=None, reconnect=True)
async def post_user_feedback(session: aiohttp.ClientSession):
    with open("store.json", "r") as store:
        try:
            data = json.load(store)
            latest_id = data[-1].get("latest_id", 0)
        except JSONDecodeError:
            return

    feedback = await get_latest_feedback(token=os.getenv("API_AUTH_TOKEN"), session=session, latest_id=latest_id)

    if len(feedback) == 0:
        print("No new feedback to broadcast.")
        return

    with open("store.json", "w+") as store:
        lastest_feedback_id = feedback[-1].get('id')

        json.dump([{"latest_id": lastest_feedback_id}], store)

    feedback_to_broadcast = [f for f in feedback if f.get('id', 0) > latest_id]

    await broadcast_feedback(feedback_to_broadcast)

    return


async def broadcast_feedback(feedback_to_broadcast: List[dict]):
    feedback_channel = bot.get_channel(841366652935471135)

    for f in feedback_to_broadcast:
        voter   = await get_player(session=session, token=os.getenv("API_AUTH_TOKEN"), player_id=f.get('voter_id'))
        subject = await get_player(session=session, token=os.getenv("API_AUTH_TOKEN"), player_id=f.get('subject_id'))

        if f.get("vote") == 1:
            embed_color=0x009302
            vote_name="Looks good!"
        elif f.get("vote") == 0:
            embed_color=0x6A6A6A
            vote_name="Not sure.."
        else:
            embed_color=0xFF0000
            vote_name="Looks wrong."

        embed = discord.Embed(title="New Feedback Submission", color=embed_color)
        embed.add_field(name="Voter Name", value=f"{voter.get('name')}", inline=False)
        embed.add_field(name="Subject Name", value=f"{subject.get('name')}", inline=False)
        embed.add_field(name="Prediction", value=f"{f.get('prediction').replace('_', ' ')}")
        embed.add_field(name="Confidence", value=f"{f.get('confidence') * 100:.2f}%")
        embed.add_field(name="Vote", value=f"{vote_name}", inline=False)
        embed.add_field(name="Explanation", value=f"{string_processing.escape_markdown(f.get('feedback_text'))}", inline=False)

        if f.get("vote") == -1 and f.get("proposed_label"):
            embed.add_field(name="Proposed Label", value=f"{f.get('proposed_label').replace('_', ' ')}")

        embed.set_footer(text=datetime.datetime.utcnow().strftime('%a %B %d %Y  %I:%M:%S %p'))
        
        await feedback_channel.send(embed=embed)
        await asyncio.sleep(2)

    return


@post_user_feedback.before_loop
async def before_post_user_feedback():
    await asyncio.sleep(5)
    print("Feedback monitoring and posting is now active.")


async def send_error_message(ctx, error, tb):
    # Cleandoc was being really annoying for this, would be multiline str but was having issues.
    error_message =  f"`{ctx.author}` running `{ctx.command}` caused `{error.__class__.__name__}`\n"
    error_message += f"Message Link: {ctx.message.jump_url}\n"
    error_message += f"```{''.join(tb)}```"

    await bot.get_channel(847578925857112064).send(error_message)


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

            post_user_feedback.start(session)
            await bot.start(os.getenv("TOKEN"))

    print("Bot is going night-night.")
    await bot.close()


uvloop.install()

asyncio.run(startup())
