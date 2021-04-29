import os
import atexit

import discord
from discord.ext import commands
from dotenv import load_dotenv

print(discord.__version__)

import reaction_commands as rc
import mesage_commands as mc

import checks as checks

import sys
import traceback

#Log File
error_file = open('error.log', 'w+')

load_dotenv()

token = os.getenv('API_AUTH_TOKEN')

description = '''It's NOT a bot. That would be quite hypocritical, wouldn't it?'''

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True

bot = commands.Bot(command_prefix=os.getenv('COMMAND_PREFIX'), description=description, intents=intents, case_insensitive=True)


# discord bot events
@bot.event
async def on_ready():
    print('We have logged in as {0}'.format(bot.user.name))


@bot.command()
async def meow(ctx):
    await mc.meow_command(ctx)


@bot.command()
async def woof(ctx):
    await mc.woof_command(ctx)


@bot.command()
async def poke(ctx):
    await mc.poke_command(ctx)


@bot.command()
async def utc(ctx):
    await mc.utc_time_command(ctx)


@bot.command()
async def lookup(ctx):
    await mc.hiscores_lookup(ctx)


@bot.command()
async def warn(ctx):
    await mc.warn_command(ctx)


@bot.command()
async def rules(ctx):
    await mc.rules_command(ctx)


@bot.command()
async def issues(ctx):
    await mc.issues_command(ctx)


@bot.command()
async def website(ctx):
    await mc.website_command(ctx)


@bot.command()
async def patreon(ctx):
    await mc.patreon_command(ctx)


@bot.command()
async def invite(ctx):
    await mc.invite_command(ctx)


@bot.command()
async def github(ctx, repo):
    await mc.github_command(ctx, repo)


@commands.check(checks.check_allowed_channel)
@bot.command()
async def link(ctx, *player_name):
    await mc.link_command(ctx, " ".join(player_name))


@commands.check(checks.check_allowed_channel)
@bot.command()
async def verify(ctx, *player_name):
    await mc.verify_comand(ctx, " ".join(player_name))


@commands.check(checks.check_allowed_channel)
@bot.command()
async def primary(ctx, *player_name):
    await mc.primary_command(ctx, " ".join(player_name))


@commands.check(checks.check_allowed_channel)
@bot.command()
async def list(ctx):
    await mc.list_command(ctx)


@commands.check(checks.check_allowed_channel)
@bot.command()
async def submit(ctx, paste_url):
    await mc.submit_command(ctx, paste_url, bot.get_user(int(os.getenv('SUBMIT_RECIPIENT'))))


@commands.check(checks.check_allowed_channel)
@bot.command()
async def region(ctx, *region_name, token=token):
    await mc.region_command(ctx, " ".join(region_name), token=token)


@commands.check(checks.check_allowed_channel)
@bot.command()
async def map(ctx, *region_name):
    await mc.map_command(ctx, " ".join(region_name))

@commands.check(checks.check_allowed_channel)
@bot.command()
async def coords(ctx, x, y, z, zoom):
    await mc.coords_command(ctx, x, y, z, zoom)


@commands.check(checks.check_allowed_channel)
@bot.command()
async def stats(ctx):
    await mc.stats_command(ctx)


@commands.check(checks.check_allowed_channel)
@bot.command()
async def kc(ctx, *player_name):
    await mc.kc_command(ctx, " ".join(player_name))


@commands.check(checks.check_allowed_channel)
@bot.command()
async def predict(ctx, *player_name):
    await mc.predict_command(ctx, " ".join(player_name))


@commands.check(checks.check_patron)
@bot.command()
async def heatmap(ctx, *region_name, token=token):
    await mc.heatmap_command(ctx, " ".join(region_name), token=token)


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


@bot.event
async def on_raw_reaction_removed(payload):
    pass


@bot.event
async def on_member_join(member):
    pass

async def get_reaction_message(reaction_payload):
    guild = bot.get_guild(reaction_payload.guild_id)
    channel = guild.get_channel(reaction_payload.channel_id)
    message = await channel.fetch_message(reaction_payload.message_id)

    return message


@atexit.register
def shutdown():
    error_file.close()
    print("Bot is going night-night.")

bot.run(os.getenv('TOKEN'))
