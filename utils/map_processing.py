
import os
from datetime import date

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import PIL
import urllib
import fnmatch
import math
from datetime import date


def region_to_wp(regionId, regionX, regionY, plane):
    return ((regionId >> 8) << 6) + regionX, ((regionId & 0xff) << 6) + regionY, plane


def plotheatmap(dfLocalBan, regionid, filename):
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
                    cmap='gnuplot_r', fill=True, bw_method=.05)
    hmap.legend([f'Bot Detector Plugin: {date.today()}'],labelcolor='white',loc='lower right')

    plt.savefig(filename, bbox_inches='tight', pad_inches = 0)
    plt.figure().clear()
    plt.close('all')

def plotPixelHeatMap(dfLocalBan, regionid, filename):
    origin_wp = region_to_wp(regionid, 0, 0, 0)
    dfLocalBan['confirmed_ban'] = dfLocalBan['confirmed_ban'].apply(lambda x : math.log(x + 1))

    np_arr = np.empty((64,64))
    np_arr[:] = np.NaN
    for i, row in dfLocalBan.iterrows():
        x_ind = int(row['x_coord']) - origin_wp[0]
        y_ind = int(row['y_coord']) - origin_wp[1]
        if (0 <= x_ind <= 63 and 0 <= y_ind <= 63):
            np_arr[y_ind, x_ind] = row['confirmed_ban']

    map_img = PIL.Image.open(urllib.request.urlopen(f'https://raw.githubusercontent.com/Bot-detector/OSRS-Visible-Region-Images/main/Region_Maps/{regionid}.png'))

    plt.style.use('seaborn-white')
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches
    plt.subplots(figsize=(512*px, 512*px))
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.axis('off')

    hmap = sns.heatmap(data=np_arr, cmap='gnuplot_r',
                    cbar=False, square=True,
                    alpha = 0.5)
    hmap.invert_yaxis()
    hmap.set_xlim([0, 64])
    hmap.set_ylim([0, 64])
    hmap.imshow(map_img, aspect=hmap.get_aspect(),
                extent=[0, 64, 0, 64], zorder=0)

    hmap.legend([f'Bot Detector Plugin: {date.today()}'],
                labelcolor='white',loc='lower right')

    plt.savefig(filename, bbox_inches='tight', pad_inches = 0)
    plt.figure().clear()
    plt.close('all')


async def CleanupImages(filename):
    os.remove(filename)


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

def cleanOldHeatmaps(region_id):
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, f"{region_id}*.png"):
            os.remove(file)

def heatmapExists(filename):
    return os.path.exists(filename)

def getFileName(region_id):
    date_str = date.today().strftime("%d-%m-%Y")
    return f"{region_id}_{date_str}.png"

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
