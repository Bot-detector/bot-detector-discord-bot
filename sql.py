import os
import mysql.connector
import string
import random
import re
import numpy as np
import requests as req
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

config_submissions = {
  'user': os.getenv('DB_USER'),
  'password': os.getenv('DB_PASS'),
  'host': os.getenv('DB_HOST'),
  'database': os.getenv('DB_NAME_SUBMISSIONS'),
}

config_players = {
  'user': os.getenv('DB_USER'),
  'password': os.getenv('DB_PASS'),
  'host': os.getenv('DB_HOST'),
  'database': os.getenv('DB_NAME_PLAYERS'),
}

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
    mydb = mysql.connector.connect(**config_submissions)
    mycursor = mydb.cursor(buffered=True)
    label_string = convert(label)
    sql = "INSERT INTO labels_submitted (Label) VALUES (%s)"
    try:
        mycursor.execute(sql, label_string)
    except:
        pass
    mydb.commit()

    mycursor.close()
    mydb.close()
    return


def name_insert(newlines):
    mydb = mysql.connector.connect(**config_submissions)
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

    mycursor.close()
    mydb.close()
    return

# recall functions 

def label_id(label):
    mydb = mysql.connector.connect(**config_submissions)
    label_string = label_clean(label)
    
    mycursor = mydb.cursor(buffered=True)
    sql = "SELECT * from labels_submitted WHERE label = %s" % str(label_string)
    mycursor.execute(sql, label_string)
    
    head_rows = mycursor.fetchmany(size=1)
    label_id = head_rows[0][0]
    
    mydb.commit()

    mycursor.close()
    mydb.close()
    return label_id


def name_id(newlines):
    mydb = mysql.connector.connect(**config_submissions)
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

    mycursor.close()
    mydb.close()
    return player_ids

# final join functions

def player_label_join(label, newlines):
    l_id = label_id(label)
    p_ids = name_id(newlines)
    mydb = mysql.connector.connect(**config_submissions)
    mycursor = mydb.cursor(buffered=True)
    for i in range(0,len(p_ids)):
        sql = "INSERT IGNORE playerlabels_submitted (Player_ID, Label_ID) VALUES (%s, %s)" % (p_ids[i], l_id)
        mycursor.execute(sql)
    mydb.commit()

    mycursor.close()
    mydb.close()
    return

################################################################################################################################################################


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
