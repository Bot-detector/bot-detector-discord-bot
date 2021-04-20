import os
import mysql.connector
import string
import random
import re
import numpy as np
import requests as req
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from collections import namedtuple

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

def convert_names(list):
    return (*list,)

def convert(list):
    return (list, )

def execute_sql(sql, insert=False, param=None):
    conn = mysql.connector.connect(**config_submissions)
    mycursor = conn.cursor(buffered=True, dictionary=True)
    
    mycursor.execute(sql, param)
    
    if insert:
        conn.commit()
        mycursor.close()
        conn.close()
        return

    rows = mycursor.fetchall()
    Record = namedtuple('Record', rows[0].keys())
    records = [Record(*r.values()) for r in rows]

    mycursor.close()
    conn.close()
    return records

def InsertPlayers(sql, List):
    mydb = mysql.connector.connect(**config_submissions)
    mycursor = mydb.cursor(buffered=True)
    
    r = list()
    for i in List:
        r.append(convert(i))
    List = r
    
    query = convert_names(List)
    mycursor.executemany(sql,query)
    
    mydb.commit()
    mycursor.close()
    mydb.close()
    return 

def InsertPlayerLabel(sqlInsertPlayerLabel, playerID, dfLabelID):
    mydb = mysql.connector.connect(**config_submissions)
    mycursor = mydb.cursor(buffered=True)
    
    LabelID = int(dfLabelID.values[0][0])
    playerID
    
    r = list()
    for i in playerID:
        r.append((i,LabelID))
    
    mycursor.executemany(sqlInsertPlayerLabel,r)
    
    mydb.commit()
    mycursor.close()
    mydb.close()
    return

def PlayerID(sqlPlayerID, List):
    mydb = mysql.connector.connect(**config_submissions)
    mycursor = mydb.cursor(buffered=True)
    
    r = list()
    for i in List:
        r.append(convert(i))
    List = r
    
    query = convert_names(List)
    
    playerID = list()
    for i in query:
        mycursor.execute(sqlPlayerID,i)
        playerID.append(mycursor.fetchone()[0])
    
    mycursor.close()
    mydb.close()
    return playerID

def get_paste_data(paste_url):
    paste_data = req.get(paste_url)
    paste_soup = BeautifulSoup(paste_data.content, 'html.parser')
    return paste_soup

def get_paste_names(paste_soup):
    Set = set()
    lines = paste_soup.findAll('textarea',{"class":"textarea"})[0].decode_contents()
    lines = lines.splitlines()
    for line in lines:
        L = re.fullmatch('[\w\d _-]{1,12}', line)
        if L:
            Set.add(line)
            
    List = Set
    return List

def get_paste_label(paste_soup):
    label = paste_soup.findAll('div',{"class":"info-top"})[0].text.strip()
    L = re.fullmatch('[\w\d _-]{1,100}', label)
    if L:
        labelCheck = label
    return labelCheck

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
  
  
################################################################################################################################################################

# !Primary sql statements

def discord_verification_check(discord_id, player_id): #custom
    mydb = mysql.connector.connect(**config_submissions)
    mycursor = mydb.cursor(buffered=True)
    verified = 0
    owner_id = 0
    verified_list = []
    
    sql = "SELECT * from discordVerification WHERE Discord_id = %s and Player_id = %s"
    query = ((discord_id),(player_id))
    mycursor.execute(sql,query)
    data = mycursor.fetchall()
    
    if len(data)>0:
        check = True
        for i in range(0,len(data)):
            verified_list = np.append(verified_list, data[i][-1])
        verified = np.max(verified_list)
    else:
        check = False

    mycursor.close()
    mydb.close()
    return check, verified

def VerifyRSNs(discord_id, player_id): #custom
    mydb = mysql.connector.connect(**config_submissions)
    mycursor = mydb.cursor(buffered=True)
    verified_account = 0
    
    sql = "Select * from discordVerification WHERE discord_id = %s and Player_id = %s"
    query = ((discord_id),(player_id))
    mycursor.execute(sql,query)
    data = mycursor.fetchall()
    if len(data)>0:
        verified_account = data[0][-1]
    else:
        pass
    mycursor.close()
    mydb.close()
    
    return data, verified_account

def insertPrimaryNULL(discord_id):
    PrimaryNULL = False
    mydb = mysql.connector.connect(**config_submissions)
    mycursor = mydb.cursor(buffered=True)

    sql = "UPDATE discordVerification SET primary_rsn = %s WHERE Discord_id = %s"
    query = ((0),(discord_id))
    mycursor.execute(sql,query)
    mydb.commit()

    mycursor.close()
    mydb.close()
    
    PrimaryNULL = True
    return PrimaryNULL

def insertPrimaryTRUE(discord_id, player_id):
    
    PrimaryTRUE = False
    
    mydb = mysql.connector.connect(**config_submissions)
    mycursor = mydb.cursor(buffered=True)

    sql = "UPDATE discordVerification SET primary_rsn = %s WHERE Discord_id = %s and Player_id = %s"
    query = ((1),(discord_id),(player_id))
    mycursor.execute(sql,query)
    mydb.commit()

    mycursor.close()
    mydb.close()
    
    PrimaryTRUE = True
    return PrimaryTRUE
  
################################################################################################################################################################

# Heatmap Statements
def getHeatmapRegion(regionName):
    mydb_players = mysql.connector.connect(**config_players)
    mycursor = mydb_players.cursor(buffered=True)

    sql = "SELECT * FROM regionIDNames WHERE region_name LIKE %s"
    regionName = "%" + regionName + "%"
    query = convert(regionName) 
    print(query)
    mycursor.execute(sql,query)
    data = mycursor.fetchall()
    
    mycursor.close()
    mydb_players.close()
    return data

def displayDuplicates(data):
    region_name = list()
    regionIDs = list()
    removedDuplicates = list()
    for i in data:
        regionIDs.append(i[1])
        region_name.append(i[3])
    removedDuplicates = list(set(region_name))
    return removedDuplicates, regionIDs, region_name

def allHeatmapSubRegions(regionTrueName, region_name, regionIDs, removedDuplicates):
    regionSelections = list()
    regionIDindices = [i for i, x in enumerate(region_name) if x == str(regionTrueName)]
    for i in regionIDindices:
        regionSelections.append(regionIDs[i])
    return regionSelections

def Autofill(removedDuplicates, regionName):
    regionShort = []
    for i in removedDuplicates:
        regionShort.append(len(i)-len(regionName))
    index = regionShort.index(np.min(regionShort))
    regionTrueName = removedDuplicates[index]
    return regionTrueName

# Last Seen Location used in Predict

def LocationgetPlayerID(playerName):
    mydb_players = mysql.connector.connect(**config_players)
    mycursor = mydb_players.cursor(buffered=True)

    sql = "SELECT id FROM Players WHERE name = %s ORDER BY id DESC LIMIT 1"
    query = convert(playerName) 
    mycursor.execute(sql,query)
    playerID = mycursor.fetchall()
    
    mycursor.close()
    mydb_players.close()
    return playerID

def LocationgetReportLocation(playerID):
    mydb_players = mysql.connector.connect(**config_players)
    mycursor = mydb_players.cursor(buffered=True)

    sql = "SELECT region_id FROM Reports WHERE reportedID = %s ORDER BY ID DESC LIMIT 1"
    query = convert(playerID[0][0]) 
    mycursor.execute(sql,query)
    reportLocation = mycursor.fetchall()
    
    mycursor.close()
    mydb_players.close()
    return reportLocation

def LocationgetReportLocationName(reportLocation):
    mydb_players = mysql.connector.connect(**config_players)
    mycursor = mydb_players.cursor(buffered=True)

    sql = "SELECT region_name FROM regionIDNames WHERE region_ID = %s ORDER BY entry_ID DESC LIMIT 1"
    query = convert(reportLocation[0][0]) 
    mycursor.execute(sql,query)
    reportLocationName = mycursor.fetchall()
    reportLocationName = reportLocationName[0][0]
    mycursor.close()
    mydb_players.close()
    return reportLocationName
