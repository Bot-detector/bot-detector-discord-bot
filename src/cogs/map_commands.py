import fnmatch
import logging
import math
import os
import urllib
from datetime import date
from inspect import cleandoc

import discord
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import PIL
import seaborn as sns
from src.config import api
from discord.ext import commands
from discord.ext.commands import Cog, Context
from src.utils.checks import PATREON_ROLE, OWNER_ROLE

logger = logging.getLogger(__name__)


class mapCommands(Cog):
    def __init__(self, bot: discord.Client) -> None:
        """
        Initialize the mapCommands class.
        :param bot: The discord bot client.
        """
        self.bot = bot

    async def __web_request(self, url: str) -> dict:
        """
        Make a web request to the specified url.

        :param url: The url to make the request to.
        :return: The response from the request.
        """
        async with self.bot.Session.get(url) as response:
            if response.status != 200:
                logger.error({"status": response.status, "url": url})
                return None
            return await response.json()

    @commands.command()
    async def region(self, ctx: Context, *, region_name: str):
        """"""
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": f"Requested region {region_name}"
        }
        logger.debug(debug)

        dataRegion = await api.get_heatmap_region(region_name=region_name)
        dfDataRegion = pd.DataFrame(dataRegion)
        dfRegion = self.__displayDuplicates(dfDataRegion)

        if len(dfRegion) == 0:
            embed = discord.Embed(
                color=discord.Colour.dark_red(),
                description=cleandoc(
                    f"""
                        {region_name} does not correspond with any of our labeled regions.
                        It is possible that we just need to add it. Please let us know if so!
                    """
                ),
            )

            return await ctx.send(embed=embed)

        if len(dfRegion) < 30:
            regionTrueName, region_id = self.__Autofill(dfRegion, region_name)

            msg = cleandoc(
                f"""```diff
                Input: {region_name}
                Selection From: {', '.join(str(elem) for elem in dfRegion['region_name'].values)}
                Selected: {regionTrueName}
            ```"""
            )
        else:
            msg = "```diff\n- More than 30 Regions selected. Please refine your search.```"

        await ctx.send(msg)

    @commands.command(aliases=["hm"])
    @commands.has_any_role(PATREON_ROLE, OWNER_ROLE)
    async def heatmap(self, ctx: Context, *, region):
        """"""
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": f"Requested heatmap {region}"
        }
        logger.debug(debug)
        if not region:
            return await ctx.send("Please enter a region name or region ID.")

        info_msg = await ctx.send("Getting that map ready for you. One moment, please!")
        await ctx.typing()

        if region.isdigit():
            regionTrueName = f"Region ID: {region}"
            mapFilePath = await self.__runAnalysis(regionTrueName, region)

            if not mapFilePath:
                await self.map(ctx=ctx, region=region)
                await ctx.reply("We have no data on this region yet.")
            else:
                try:
                    await ctx.reply(file=discord.File(mapFilePath))
                except Exception as e:
                    print(e)
                    await ctx.reply(
                        "Uhhh... I should have a heatmap to give you, but I don't. Please accept this image of a cat fixing our bot instead."
                    )
                    await ctx.reply("https://i.redd.it/lel3o4e2hhp11.jpg")

        else:
            dataRegion = await api.get_heatmap_region(region_name=region)
            dfDataRegion = pd.DataFrame(dataRegion)
            dfRegion = self.__displayDuplicates(dfDataRegion)

            if not len(dfRegion):
                embed = discord.Embed(
                    description=cleandoc(
                        f"""
                        "{region}" does not correspond with any of our labeled regions.
                        It is possible that we just need to add it. Please let us know if so!
                    """
                    ),
                    color=discord.Colour.dark_red(),
                )

                return await ctx.reply(embed=embed)

            if len(dfRegion) < 30:
                regionTrueName, region_id = self.__Autofill(dfRegion, region)
                mapFilePath = await self.__runAnalysis(regionTrueName, region_id)

                if not mapFilePath:
                    await self.map(ctx=ctx, region=region)
                    await ctx.reply("We have no data on this region yet.")

                else:
                    try:
                        await ctx.reply(file=discord.File(mapFilePath))
                    except:
                        await ctx.reply(
                            "Uhhh... I should have a heatmap to give you, but I don't. Please accept this image of a cat fixing our bot instead."
                        )
                        await ctx.reply("https://i.redd.it/lel3o4e2hhp11.jpg")

            else:
                msg = ">30 Regions selected. Please refine your search."
                await ctx.reply(msg)

        await info_msg.delete()

    @commands.command("map")
    async def map(self, ctx: Context, *, region=None):
        """"""
        debug = {
            "author": ctx.author.name,
            "author_id": ctx.author.id,
            "msg": f"Requested map {region}"
        }
        logger.debug(debug)
        if not region:
            return await ctx.send("Please enter a region name or region ID.")

        if region.isdigit():
            msg = f"https://raw.githubusercontent.com/Ferrariic/OSRS-Visible-Region-Images/main/Region_Maps/{region}.png"

        else:
            dataRegion = await api.get_heatmap_region(region_name=region)
            dfDataRegion = pd.DataFrame(dataRegion)
            dfRegion = self.__displayDuplicates(dfDataRegion)

            if len(dfRegion) == 0:
                embed = discord.Embed(
                    description=cleandoc(
                        f"""
                        "{region}" does not correspond with any of our labeled regions.
                        It is possible that we just need to add it. Please let us know if so!
                    """
                    ),
                    color=discord.Colour.dark_red(),
                )

                return await ctx.send(embed=embed)

            if len(dfRegion) < 30:
                regionTrueName, region_id = self.__Autofill(dfRegion, region)
                msg = f"https://raw.githubusercontent.com/Ferrariic/OSRS-Visible-Region-Images/main/Region_Maps/{region_id}.png"
            else:
                msg = "```diff\n- More than 30 Regions selected. Please refine your search.```"

        await ctx.send(msg)

    # Analysis run for map_processing Heatmap
    async def __runAnalysis(self, regionTrueName, region_id):
        filename = self.__getFileName(region_id=region_id)

        if self.__heatmapExists(filename=filename):
            return filename
        else:
            self.__cleanOldHeatmaps(region_id=region_id)

        region_id = int(region_id)

        data = await api.get_heatmap_data(region_id=region_id)
        df = pd.DataFrame(data)

        if df.empty:
            return False

        if "confirmed_ban" in df.columns:
            try:
                self.__plotHeatmap(dfLocalBan=df, regionid=region_id, filename=filename)
            except ValueError:
                self.__plotPixelHeatMap(
                    dfLocalBan=df, regionid=region_id, filename=filename
                )
            except Exception:
                return False

        return filename

    def __regionToWorldPoint(self, regionId, regionX, regionY, plane):
        return (
            ((regionId >> 8) << 6) + regionX,
            ((regionId & 0xFF) << 6) + regionY,
            plane,
        )

    def __plotHeatmap(self, dfLocalBan, regionid, filename):
        origin_wp = self.__regionToWorldPoint(regionid, 0, 0, 0)
        bounds_x = (origin_wp[0] - 0.5, origin_wp[0] + 63.5)
        bounds_y = (origin_wp[1] - 0.5, origin_wp[1] + 63.5)

        # Optionally, apply log to values (+1 first to avoid 0 weigth when val == 1)
        dfLocalBan["confirmed_ban"] = dfLocalBan["confirmed_ban"].apply(
            lambda x: math.log(x + 1)
        )

        map_img = PIL.Image.open(
            urllib.request.urlopen(
                f"https://raw.githubusercontent.com/Bot-detector/OSRS-Visible-Region-Images/main/Region_Maps/{regionid}.png"
            )
        )

        plt.style.use("seaborn-white")
        px = 1 / plt.rcParams["figure.dpi"]  # pixel in inches
        plt.subplots(figsize=(512 * px, 512 * px))
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)
        plt.xlim(bounds_x)
        plt.ylim(bounds_y)
        plt.imshow(map_img, zorder=0, extent=[*bounds_x, *bounds_y])
        plt.axis("off")

        hmap = sns.kdeplot(
            data=dfLocalBan,
            x="x_coord",
            y="y_coord",
            weights="confirmed_ban",
            gridsize=256,
            alpha=0.625,
            levels=256,
            antialiased=True,
            cmap="gnuplot_r",
            fill=True,
            bw_method=0.05,
        )
        hmap.legend(
            [f"Bot Detector Plugin: {date.today()}"],
            labelcolor="white",
            loc="lower right",
        )

        plt.savefig(filename, bbox_inches="tight", pad_inches=0)
        plt.figure().clear()
        plt.close("all")

    def __plotPixelHeatMap(self, dfLocalBan, regionid, filename):
        origin_wp = self.__regionToWorldPoint(regionid, 0, 0, 0)
        dfLocalBan["confirmed_ban"] = dfLocalBan["confirmed_ban"].apply(
            lambda x: math.log(x + 1)
        )

        np_arr = np.empty((64, 64))
        np_arr[:] = np.NaN
        for i, row in dfLocalBan.iterrows():
            x_ind = int(row["x_coord"]) - origin_wp[0]
            y_ind = int(row["y_coord"]) - origin_wp[1]
            if 0 <= x_ind <= 63 and 0 <= y_ind <= 63:
                np_arr[y_ind, x_ind] = row["confirmed_ban"]

        map_img = PIL.Image.open(
            urllib.request.urlopen(
                f"https://raw.githubusercontent.com/Bot-detector/OSRS-Visible-Region-Images/main/Region_Maps/{regionid}.png"
            )
        )

        plt.style.use("seaborn-white")
        px = 1 / plt.rcParams["figure.dpi"]  # pixel in inches
        plt.subplots(figsize=(512 * px, 512 * px))
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)
        plt.axis("off")

        hmap = sns.heatmap(
            data=np_arr, cmap="gnuplot_r", cbar=False, square=True, alpha=0.5
        )
        hmap.invert_yaxis()
        hmap.set_xlim([0, 64])
        hmap.set_ylim([0, 64])
        hmap.imshow(map_img, aspect=hmap.get_aspect(), extent=[0, 64, 0, 64], zorder=0)

        hmap.legend(
            [f"Bot Detector Plugin: {date.today()}"],
            labelcolor="white",
            loc="lower right",
        )

        plt.savefig(filename, bbox_inches="tight", pad_inches=0)
        plt.figure().clear()
        plt.close("all")

    def __displayDuplicates(self, df):
        dfRegion = df.drop_duplicates(subset=["region_name"], keep="first")
        return dfRegion

    def __cleanOldHeatmaps(self, region_id):
        for file in os.listdir("."):
            if fnmatch.fnmatch(file, f"{region_id}*.png"):
                os.remove(file)

    def __heatmapExists(self, filename):
        return os.path.exists(filename)

    def __getFileName(self, region_id):
        date_str = date.today().strftime("%d-%m-%Y")
        return f"{region_id}_{date_str}.png"

    def __Autofill(self, dfRegion, regionName):
        regionShort = []
        name_index = dfRegion["region_name"].values
        location_index = dfRegion["region_ID"].values
        for i in name_index:
            regionShort.append(len(i) - len(regionName))
        index = regionShort.index(np.min(regionShort))
        regionTrueName = name_index[index]
        region_id = location_index[index]
        return regionTrueName, region_id
