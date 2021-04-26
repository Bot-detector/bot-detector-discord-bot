import os
import os.path
from collections import namedtuple
from datetime import date

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
# custom
import sql

load_dotenv()

token = os.getenv('API_AUTH_TOKEN')

# TODO: Refactor all this
def execute_sql(sql, insert=False, param=None):
    conn = mysql.connector.connect(**config_players)
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

def convertGlobaltoLocal(regionid, df):
    dfLocal = pd.DataFrame(columns=['player_ids','local_x','local_y'])
    
    regionColumnShift = 256
    startRegion = 4627
    x_startSW = 1152
    y_startSW = 1215
    gridShiftLocal = 64

    ycolumnglobal = gridShiftLocal*regionColumnShift
    rawcoord = (regionid-startRegion)/regionColumnShift

    xshiftnormal = rawcoord - (rawcoord % 1)
    yshiftnormal = rawcoord % 1

    xLocalOrigin = x_startSW + xshiftnormal*gridShiftLocal
    yLocalOrigin = y_startSW + ycolumnglobal*yshiftnormal + 1

    dfLocal['local_x'] = df['x_coord'] - xLocalOrigin
    dfLocal['local_y'] = df['y_coord'] - yLocalOrigin
    return dfLocal

def plotheatmap(dfLocalBan, dfLocalReal, regionid, regionname):
    sns.set(style="ticks", context="notebook")
    plt.style.use("seaborn-white")
    plt.figure(figsize = (5,5))
    
    map_img = mpimg.imread(f'https://raw.githubusercontent.com/Ferrariic/OSRS-Visible-Region-Images/main/Region_Maps/{regionid}.png') 

    hmax = sns.kdeplot(x = dfLocalReal.local_x, y = dfLocalReal.local_y, alpha=.7, cmap="winter_r", shade=True, bw=.1)
    hmax.set(xlabel='Local X', ylabel='Local Y')
    
    hmax = sns.kdeplot(x = dfLocalBan.local_x, y = dfLocalBan.local_y, alpha=.7, cmap="autumn_r", shade=True, bw=.1)
    hmax.set(xlabel='', ylabel='',title='')
    
    hmax.legend([f'Bot Detector Plugin: {date.today()}'],labelcolor='white',loc='lower right')
    
    hmax.tick_params(axis='x', which='both', bottom='off',top='off',labelbottom='off')
    hmax.set_xticklabels([''])
    hmax.set_yticklabels([''])
    
    plt.imshow(map_img, zorder=0, extent=[0.0, 64.0, 0.0, 64.0])
    plt.axis('off')
    plt.savefig(f'{os.getcwd()}/{regionid}.png', bbox_inches='tight',pad_inches = 0)
    plt.figure().clear()
    plt.close("all")
    return

def CleanupImages(regionSelections):
    regionid = regionSelections[0]
    os.remove(f'{os.getcwd()}/{regionid}.png')
    return

def getHeatmapRegion(regionName, token):
    json = {
        'region' : regionName
    }
    url = f'https://www.osrsbotdetector.com/dev/discord/region/{token}'
    data = requests.get(url,json=json)
    return data

def getHeatmapData(region_id, token):
    json = {
        'region_id' : region_id
    }
    url = f'https://www.osrsbotdetector.com/dev/discord/heatmap/{token}'
    data = requests.get(url,json=json)
    return data

def displayDuplicates(df):
    dfRegion = df.drop_duplicates(subset=['region_name'], keep='first')
    return dfRegion

def Autofill(dfRegion, regionName):
    regionShort = []
    name_index = dfRegion['region_name'].values
    location_index = dfRegion['region_ID'].values
    for i in name_index:
        regionShort.append(len(i)-len(regionName))
    index = regionShort.index(np.min(regionShort))
    regionTrueName = name_index[index]
    region_id = location_index[index]
    return regionTrueName, region_id
