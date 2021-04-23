import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

print(discord.__version__)

import reaction_commands as rc
import mesage_commands as mc

import checks as checks

load_dotenv()

description = '''It's NOT a bot. That would be quite hypocritical, wouldn't it?'''

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)


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
async def link(ctx, player_name):
    await mc.link_command(ctx, player_name)


@commands.check(checks.check_allowed_channel)
@bot.command()
async def verify(ctx, player_name):
    await mc.verify_comand(ctx, player_name)


@commands.check(checks.check_allowed_channel)
@bot.command()
async def primary(ctx, player_name):
    await mc.primary_command(ctx, player_name)


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
async def region(ctx, region_name):
    await mc.region_command(ctx, region_name)


@commands.check(checks.check_allowed_channel)
@bot.command()
async def map(ctx, region_name):
    await mc.map_command(ctx, region_name)


@commands.check(checks.check_allowed_channel)
@bot.command()
async def stats(ctx):
    await mc.stats_command(ctx)


@commands.check(checks.check_allowed_channel)
@bot.command()
async def kc(ctx, player_name):
    await mc.kc_command(ctx, player_name)


@commands.check(checks.check_allowed_channel)
@bot.command()
async def predict(ctx, player_name):
    await mc.predict_command(ctx, player_name)


@commands.check(checks.check_allowed_channel)
@bot.command()
async def heatmap(ctx, region_name):
    await mc.heatmap_command(ctx, region_name)


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


@bot.event
async def on_raw_reaction_add(payload):
    await rc.add_prediction_feedback(payload,
                                     await get_reaction_message(payload))


@bot.event
async def on_command_error(ctx, error):
    await ctx.channel.send(error)


@bot.event
async def on_raw_reaction_removed(payload):
    print("REMOVED")
    print(payload)


@bot.event
async def on_member_join(member):
    pass


def parse_command(cmd):
    cmd_split = cmd.split(" ", 1)

    command = {
        "name": cmd_split[0].lower(),
        "params": None
    }

    if (len(cmd_split) > 1):
        command['params'] = cmd_split[1]

    return command


async def get_reaction_message(reaction_payload):
    guild = bot.get_guild(reaction_payload.guild_id)
    channel = guild.get_channel(reaction_payload.channel_id)
    message = await channel.fetch_message(reaction_payload.message_id)

    return message


bot.run(os.getenv('TOKEN'))
