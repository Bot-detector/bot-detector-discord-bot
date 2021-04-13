import discord
print(discord.__version__)
import os
import json
from dotenv import load_dotenv
import re
import requests as req
from bs4 import BeautifulSoup
import mysql.connector
import logging
import string
import random
import numpy as np

from mesage_commands import *

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

host_ip = os.getenv('DB_HOST')
user_id = os.getenv('DB_USER')
password_id = os.getenv('DB_PASS')
database_id = os.getenv('DB_NAME')

config_submissions = {
  'user': user_id,
  'password': password_id,
  'host': host_ip,
  'database': os.getenv('DB_NAME_SUBMISSIONS'),
}

config_players = {
  'user': user_id,
  'password': password_id,
  'host': host_ip,
  'database': os.getenv('DB_NAME_PLAYERS'),
}

# sql functions #########################################################################################################################################################

def get_paste_names(paste_url):
    newlines = list()
    data = req.get(paste_url)
    soup = BeautifulSoup(data.content, 'html.parser')
    
    lines = soup.findAll('textarea',{"class":"textarea"})[0].decode_contents()
    lines = lines.splitlines()
    
    label = soup.findAll('title')[0].decode_contents()
    label = label[:-15]
    
    for line in lines:
        L = re.fullmatch('[\w\d _-]{1,12}', line)
        if L:
            newlines.append(line)
            
    return newlines, label

# pre-processing 

def convert(list):
    return (list, )


def convert_names(list):
    return (*list,)


def label_clean(label):
    label_string = '"' + str(label) + '"'
    return label_string


def name_clean(newlines):
    line_set = list()
    for line in newlines:
        str_line = '"' + str(line) + '"'
        line_set.append(str_line)
    return line_set

# insert functions

def label_insert(label):
    mycursor = mydb.cursor(buffered=True)
    label_string = convert(label)
    sql = "INSERT INTO labels_submitted (Label) VALUES (%s)"
    try:
        mycursor.execute(sql, label_string)
    except:
        pass
    mydb.commit()
    return


def name_insert(newlines):
    mycursor = mydb.cursor(buffered=True)
    line_set = convert_names(newlines)
    sql = "INSERT INTO players_submitted (Players) VALUES (%s)"
    for i in line_set:
        try:
            i_c = convert(i)
            mycursor.execute(sql, i_c)
        except:
            pass
    mydb.commit()
    return

# recall functions 

def label_id(label):
    label_string = label_clean(label)
    
    mycursor = mydb.cursor(buffered=True)
    sql = "SELECT * from labels_submitted WHERE label = %s" % str(label_string)
    mycursor.execute(sql, label_string)
    
    head_rows = mycursor.fetchmany(size=1)
    label_id = head_rows[0][0]
    
    mydb.commit()
    return label_id


def name_id(newlines):
    player_ids = []
    line_set = name_clean(newlines)
    
    mycursor = mydb.cursor(buffered=True)
    
    for i in range(0,len(line_set)):
        sql = "SELECT * from players_submitted WHERE Players = (%s)" % line_set[i]
        mycursor.execute(sql)
        head_rows = mycursor.fetchmany(size=1)
        player_id = head_rows[0][0]
        player_ids.append(player_id)
    
    mydb.commit()
    return player_ids

# final join functions

def player_label_join(label, newlines):
    l_id = label_id(label)
    p_ids = name_id(newlines)
    mycursor = mydb.cursor(buffered=True)
    for i in range(0,len(p_ids)):
        sql = "INSERT IGNORE playerlabels_submitted (Player_ID, Label_ID) VALUES (%s, %s)" % (p_ids[i], l_id)
        mycursor.execute(sql)
    mydb.commit()
    return

################################################################################################################################################################

# !predict command color changer 

def plus_minus(var, compare):
    diff_control = '-'
    if(isinstance(var, float)):
        if(var > compare):
            diff_control = '+'
    if(isinstance(var, str)):
        if(str(var)==str(compare)):
            diff_control = '+'
    return diff_control

# ID Generator command

def id_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
  
# Verification sql statements
  
def verificationPull(playerName):
    mydb_players = mysql.connector.connect(**config_players)
    mycursor = mydb_players.cursor(buffered=True)
    
    player_id = 0
    exists = False
    
    sql = "SELECT * FROM Players WHERE name = %s"
    mycursor.execute(sql,convert(playerName))
    data = mycursor.fetchmany(size=1)
    if len(data)>0:
        exists = True
        player_id = data[0][0]
    else:
        exists = False
    
    mycursor.close()
    mydb_players.close()
    return player_id, exists

def verification_check(player_id):
    mydb = mysql.connector.connect(**config_submissions)
    mycursor = mydb.cursor(buffered=True)
    
    verified = 0
    owner_id = 0
    verified_list = []
    owner_list = []
    
    sql = "SELECT * from discordVerification WHERE Player_id = %s"
    mycursor.execute(sql,convert(player_id))
    data = mycursor.fetchall()
    print(len(data))
    
    if len(data)>0:
        check = True
        for i in range(0,len(data)):
            verified_list = np.append(verified_list, data[i][-1])
            print(data[i][1])
            owner_list = np.append(owner_list, data[i][1])
        verified = np.max(verified_list)
        owner_list = np.unique(owner_list)
    else:
        check = False

    mycursor.close()
    mydb.close()
    return check, verified, owner_list

def verificationInsert(discord_id, player_id, code):
    mydb = mysql.connector.connect(**config_submissions)
    mycursor = mydb.cursor(buffered=True)
    
    sql = "INSERT INTO discordVerification (Discord_id, Player_id, Code) VALUES (%s, %s, %s)"
    query = ((discord_id),(player_id),(code))
    mycursor.execute(sql,query)
    mydb.commit()
    
    mycursor.close()
    mydb.close()
    return

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
      
        if message.content.startswith('!link') or message.content.startswith('!Link'):
          playerName = message.content[6:18]
          owner_id = 0
          code = id_generator()
          discord_id = message.author.id

          msgPassed = "```diff" + "\n" \
          + "====== INFO ======\n" \
          + "Request to link: " + str(playerName) + "\n" \
          + "Your discord ID is: " + str(discord_id) + "\n" \
          + "====== SETUP ======\n" \
          + "+ Please submit the access code below in the form of a DM in-game to 'Ferrariic' or in the clan chat 'Bot Detector'." + "\n" \
          + "+ Access Code: " + str(code)+ "\n" \
          + "+ A message will be sent to you on Discord when your account has been successfully paired." + "\n" \
          + "====== NOTICE ======\n" \
          + "- If this RSN was submitted in error, please type !link <Your Correct RSN>" + "\n" \
          + "- This code will expire in 24 hours." + "\n" \
          + "- Do not share this code with anyone." + "\n" \
          + "```"

          msgInUse = "```diff" + "\n" \
          + "- RSN is currently in use. Please contact an Administrator" + "\n" \
          + "```"

          msgInstallPlugin = "```diff" + "\n" \
          + "- This user has not installed the Bot Detector plugin, or this user does not exist." + "\n" \
          + "- Please install the plugin or re-enter your !link <RSN> command." + "\n" \
          + "```"

          msgVerified = "```diff" + "\n" \
          + "+ Player: " + str(playerName) + "\n" \
          + "====== Verification Information ======\n" \
          + "+ Player is: Verified." + "\n" \
          + "```"

          msgUnverified = "```diff" + "\n" \
          + "+ Player: " + str(playerName) + "\n" \
          + "====== Verification Information ======\n" \
          + "- Player is: Unverified." + "\n" \
          + "```"

          player_id, exists = verificationPull(playerName)
          if exists:
              check, verified, owner_list = verification_check(player_id)
              if verified:
                  msg = msgVerified
              else:
                  if check:
                      if int(discord_id) not in owner_list:
                          verificationInsert(discord_id, player_id, code)
                          msg = msgPassed
                      else:
                          msg = msgInUse
                  else:
                      verificationInsert(discord_id, player_id, code)
                      msg = msgPassed
          else:
              msg = msgInstallPlugin

          await message.author.send(msg)

        if message.content.startswith('!verify') or message.content.startswith('!Verify'):
            playerName = message.content[8:20]
            owner_id = 0
            
            msgVerified = "```diff" + "\n" \
            + "+ Player: " + str(playerName) + "\n" \
            + "====== Verification Information ======\n" \
            + "+ Player is: Verified." + "\n" \
            + "```"

            msgUnverified = "```diff" + "\n" \
            + "+ Player: " + str(playerName) + "\n" \
            + "====== Verification Information ======\n" \
            + "- Player is: Unverified." + "\n" \
            + "```"
            
            player_id, exists = verificationPull(playerName)
            if exists:
                check, verified, owner_list = verification_check(player_id)
                if verified:
                    msg = msgVerified
                else:
                    msg = msgUnverified
            else:
                msg = msgUnverified
            
            await message.channel.send(msg)
     
        if message.content.startswith('!list') or message.content.startswith('!List'):
            msg = "Please send a link to a Pastebin URL containing your name list." + "\n" \
            + "Example: !submit https://pastebin.com/iw8MmUzg" + "\n" \
            + "___________" + "\n" \
            + "Acceptable Formatting:" + "\n" \
            + "Player 1" + "\n" \
            + "Player 2" + "\n" \
            + "Player 3" + "\n" \
            + "Player 4" + "\n" \
            + "Player 5" + "\n" \
            + "___________" + "\n" \
            + "Pastebin Settings:" + "\n" \
            + "Syntax Highlighting: None" + "\n" \
            + "Paste Expiration: 1 Day" + "\n" \
            + "Paste Exposure: Public" + "\n" \
            + "Folder: No Folder Selected" + "\n" \
            + "Password: {leave blank - no password needed}" + "\n" \
            + "Paste Name / Title: {Include your Label Here}" + "\n" 
            await message.author.send(msg)

        if message.content.startswith('!submit') or message.content.startswith('!Submit'):
            paste_url = message.content[8:100]

            newlines, label = get_paste_names(paste_url)
            label_insert(label)
            name_insert(newlines)
            player_label_join(label, newlines)

            msg = "Paste Information" + "\n" \
                + "_____________________" + "\n" \
                + "Number of Names: " + str(len(newlines)) + "\n" \
                + "Label: " + str(label) + "\n" \
                + "Samples: " + str(newlines[0:10]) + "\n" \
                + "Link: " + str(paste_url) + "\n"

            user = client.get_user(int(os.getenv('SUBMIT_RECIPIENT')))

            await user.send(msg)

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
