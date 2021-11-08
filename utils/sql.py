import os
import re
from collections import namedtuple

import mysql.connector
import numpy as np
import requests as req
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

config_submissions = {
  'user':       os.getenv('DB_USER'),
  'password':   os.getenv('DB_PASS'),
  'host':       os.getenv('DB_HOST'),
  'database':   os.getenv('DB_NAME_SUBMISSIONS'),
}

config_players = {
  'user':       os.getenv('DB_USER'),
  'password':   os.getenv('DB_PASS'),
  'host':       os.getenv('DB_HOST'),
  'database':   os.getenv('DB_NAME_PLAYERS'),
}

############################### !submit command

class Error(Exception):
    pass

class MissingNamesError(Error):
    pass

class InvalidPasteTitleError(Error):
    pass

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

    if len(Set) == 0:
        raise MissingNamesError

    return Set


def get_ghostbin_paste_names(paste_soup):
    Set = set()
    lines = paste_soup.select('body > div.container > textarea').pop().decode_contents()
    lines = lines.splitlines()

    for line in lines:
        L = re.fullmatch('[\w\d _-]{1,12}', line)
        if L:
            Set.add(line)

    if len(Set) == 0:
        raise MissingNamesError

    return Set


def get_paste_label(paste_soup):
    label = paste_soup.findAll('div',{"class":"info-top"})[0].text.strip()
    return label.replace('/', "_").replace('\0', '_')


def get_ghostbin_label(paste_soup):
    label = paste_soup.select('body > div.container > h4').pop().text.strip().replace('raw', '')
    return label.replace('/', "_").replace('\0', '_')