import discord
print(discord.__version__)
from dotenv import load_dotenv
import logging

from mesage_commands import *
from sql import *

load_dotenv()

intents = discord.Intents.default()
intents.members = True
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

    if(message.content[0] != '!'):
        return

    command = parse_command(message.content)

    if(command['name'] not in VALID_COMMANDS):
        await message.channel.send(command['name'] + " is not a valid command.")
        return

    #fun commands

    if command['name'].lower() == "!meow":
        await meow_command(message)

    if command['name'].lower() == "!poke":
        await poke_command(message)
        
    # admin commands

    if message.content.lower() == "!warn":
        await warn_command(message)
        
    # channel links
        
    if command['name'].lower() == "!rules":
        await rules_command(message)
        
    if command['name'].lower() == "!issues":
        await issues_command(message)
        
    # Web links

    if command['name'].lower() == "!website":
        await website_command(message)

    if command['name'].lower() == "!patreon":
        await patreon_command(message)

    if command['name'].lower() == "!github":
        await github_command(message, command['params'])

    if command['name'].lower() == "!invite":
        await invite_command(message)
        
    # Locked-Channel commands
        
    if message.channel.id == 825189024074563614 or message.channel.type == 'dm':
      
        if command['name'].lower() == "!link":
            await link_command(message, command['params'])

        if command['name'].lower() == "!verify":
            await verify_comand(message, command['params'])
     
        if command['name'].lower() == "!list":
            await list_command(message)

        if command['name'].lower() == "!submit":
            await submit_command(message, command['params'], 
                client.get_user(int(os.getenv('SUBMIT_RECIPIENT'))))

      # plugin and database stats

        if command['name'].lower() == "!stats":
            await stats_command(message)

      # player stats

        if command['name'].lower() == "!kc":
            await kc_command(message, command['params'])
            
      #predict method

        if command['name'].lower() == "!predict":
            await predict_command(message, command['params'])
       
          
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

client.run(os.getenv('TOKEN'))
