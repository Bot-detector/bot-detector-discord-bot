
import os
from datetime import date

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import PIL
import urllib
import math
from datetime import date


def region_to_wp(regionId, regionX, regionY, plane):
    return ((regionId >> 8) << 6) + regionX, ((regionId & 0xff) << 6) + regionY, plane


def plotheatmap(dfLocalBan, regionid, regionname):
    origin_wp = region_to_wp(regionid, 0, 0, 0)
    bounds_x = (origin_wp[0] - 0.5, origin_wp[0] + 63.5)
    bounds_y = (origin_wp[1] - 0.5, origin_wp[1] + 63.5)

    # Optionally, apply log to values (+1 first to avoid 0 weigth when val == 1)
    dfLocalBan['confirmed_ban'] = dfLocalBan['confirmed_ban'].apply(lambda x : math.log(x + 1))

    map_img = PIL.Image.open(urllib.request.urlopen(f'https://raw.githubusercontent.com/Bot-detector/OSRS-Visible-Region-Images/main/Region_Maps/{regionid}.png'))

    plt.style.use('seaborn-white')
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches
    plt.subplots(figsize=(512*px, 512*px))
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.xlim(bounds_x)
    plt.ylim(bounds_y)
    plt.imshow(map_img, zorder=0, extent=[*bounds_x, *bounds_y])
    plt.axis('off')

    hmap = sns.kdeplot(data=dfLocalBan, x='x_coord', y='y_coord', weights='confirmed_ban',
                    gridsize=256, alpha=.625, levels=256, antialiased=True,
                    cmap='autumn_r', fill=True, bw_method=.05)
    hmap.legend([f'Bot Detector Plugin: {date.today()}'],labelcolor='white',loc='lower right')

    plt.savefig(f'{regionid}.png', bbox_inches='tight', pad_inches = 0)
    plt.figure().clear()
    plt.close('all')


async def CleanupImages(regionid):
    os.remove(f'{os.getcwd()}/{regionid}.png')


async def getHeatmapRegion(session, regionName, token):
    json = {"region" : regionName}
    url = f'https://www.osrsbotdetector.com/api/discord/region/{token}/{regionName}'

    async with session.get(url,json=json) as r:
        if r.status == 200:
            data = await r.json()
            return data
            

async def getHeatmapData(session, region_id, token):
    json = {"region_id" : region_id}
    #url = f'https://www.osrsbotdetector.com/api/discord/heatmap/{token}'
    url = f'http://localhost:5000/discord/heatmap/{token}'

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
