import discord
print(discord.__version__)
from dotenv import load_dotenv
import logging

from reaction_commands import *
from mesage_commands import *
from sql import *
from patron import *

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
client = discord.Client(intents=intents)

# discord client events

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    # easter eggs
        
    if "a round of wintertodt is about to begin" in message.content.lower():
        await message.channel.send('Chop chop!')
    
    if "25 buttholes" in message.content.lower():
        await message.channel.send('hahahahahaha w0w!')

    #########################
    # ALL COMMANDS GO BELOW #
    #########################

    if(len(message.content) <= 0):
        return

    if(message.content[0] != '!'):
        return

    command = parse_command(message.content)

    #fun commands

    if command['name'].lower() == "!meow":
        await meow_command(message)
        return

    if command['name'].lower() == "!woof":
        await woof_command(message)
        return

    if command['name'].lower() == "!poke":
        await poke_command(message)
        return

    if command['name'].lower() == "!utc":
        await utc_time_command(message)
        return
        
    # admin commands

    if message.content.lower() == "!warn":
        await warn_command(message)
        return
        
    # channel links
        
    if command['name'].lower() == "!rules":
        await rules_command(message)
        return
        
    if command['name'].lower() == "!issues":
        await issues_command(message)
        return
        
    # Web links

    if command['name'].lower() == "!website":
        await website_command(message)
        return

    if command['name'].lower() == "!patreon":
        await patreon_command(message)
        return

    if command['name'].lower() == "!github":
        await github_command(message, command['params'])
        return

    if command['name'].lower() == "!invite":
        await invite_command(message)
        return
        
    # Locked-Channel commands
        
    if message.channel.id == 825189024074563614 or message.channel.id == 833479046821052436 \
        or message.channel.id == 822589004028444712 or message.channel.id == 830783778325528626 \
        or message.channel.id == 834028368147775488 or  message.channel.type == 'dm':
      
        if command['name'].lower() == "!link":
            await link_command(message, command['params'])
            return

        if command['name'].lower() == "!verify":
            await verify_comand(message, command['params'])
            return
            
        if command['name'].lower() == "!primary":
            await primary_command(message, command['params'])
            return
     
        if command['name'].lower() == "!list":
            await list_command(message)
            return

        if command['name'].lower() == "!submit":
            await submit_command(message, command['params'], 
                client.get_user(int(os.getenv('SUBMIT_RECIPIENT'))))
            return
            
      # map command
        if command['name'].lower() == "!region":
            await region_command(message, command['params'])
            return
    
        if command['name'].lower() == "!map":
            await map_command(message, command['params'])
            return
    
      # plugin and database stats

        if command['name'].lower() == "!stats":
            await stats_command(message)
            return

      # player stats

        if command['name'].lower() == "!kc":
            await kc_command(message, command['params'])
            return
            
      #predict method

        if command['name'].lower() == "!predict":
            await predict_command(message, command['params'])
            return
            
    if message.channel.id == 830783778325528626 or message.channel.id == 833479046821052436 \
        or message.channel.id == 822589004028444712 or message.channel.id == 834028368147775488 \
        or message.channel.type == 'dm':
        
        if command['name'].lower() == "!heatmap":
            await heatmap_command(message, command['params'])
            return


    #If the !command doesn't match any of the above we send this.
    await message.channel.send(command['name'] + " is not a valid command.")
    
@client.event
async def on_raw_reaction_add(payload):
    
    await add_prediction_feedback(payload,
        await get_reaction_message(payload))

@client.event
async def on_raw_reaction_removed(payload):
    print("REMOVED")
    print(payload)
       
          
@client.event
async def on_member_join(member):
    pass

def parse_command(cmd):
    cmd_split = cmd.split(" ", 1)

    command = {
        "name": cmd_split[0].lower(),
        "params": None
    }

    if(len(cmd_split) > 1):
        command['params']= cmd_split[1]

    return command

async def get_reaction_message(reaction_payload):
    guild = client.get_guild(reaction_payload.guild_id)
    channel = guild.get_channel(reaction_payload.channel_id)
    message = await channel.fetch_message(reaction_payload.message_id)

    return message

client.run(os.getenv('TOKEN'))
