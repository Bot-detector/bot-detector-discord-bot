
import os
from datetime import date

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import PIL
import urllib


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

def plotheatmap(dfLocalBan, regionid, regionname):
    sns.set(style="ticks", context="notebook")
    plt.style.use("seaborn-white")
    plt.figure(figsize = (5,5))

    map_img = PIL.Image.open(urllib.request.urlopen(f'https://raw.githubusercontent.com/Bot-detector/OSRS-Visible-Region-Images/main/Region_Maps/{regionid}.png'))

    hmax = sns.kdeplot(x = dfLocalBan.local_x, y = dfLocalBan.local_y, alpha=.4, cmap="autumn_r", shade=True, bw_method=0.05)
    hmax.set(xlabel='', ylabel='',title='')

    hmax.legend([f'Bot Detector Plugin: {date.today()}'],labelcolor='white',loc='lower right')

    plt.imshow(map_img, zorder=0, extent=[0.0, 64.0, 0.0, 64.0])
    plt.axis('off')
    plt.savefig(f'{os.getcwd()}/{regionid}.png', bbox_inches='tight',pad_inches = 0)
    plt.figure().clear()
    plt.close("all")


async def CleanupImages(region_id):
    os.remove(f'{os.getcwd()}/{region_id}.png')


async def getHeatmapRegion(session, regionName, token):
    json = {"region" : regionName}
    url = f'https://www.osrsbotdetector.com/api/discord/region/{token}/{regionName}'

    async with session.get(url,json=json) as r:
        if r.status == 200:
            data = await r.json()
            return data
            

async def getHeatmapData(session, region_id, token):
    json = {"region_id" : region_id}

    url = f'https://www.osrsbotdetector.com/api/discord/heatmap/{token}'

    async with session.get(url,json=json) as r:
        if r.status == 200:
            data = await r.json()
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
