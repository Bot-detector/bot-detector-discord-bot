import os
from inspect import cleandoc

import discord
import pandas as pd
from discord.ext import commands
from dotenv import load_dotenv

import help_messages
from utils import map_processing, string_processing, CommonCog, checks


load_dotenv()
token = os.getenv('API_AUTH_TOKEN')

class MapCommands(CommonCog, name='Map Commands'):
    cog_check = checks.check_allowed_channel

    @commands.command(description=help_messages.region_help_msg)
    async def region(self, ctx, *, regionName):
        dataRegion = await map_processing.getHeatmapRegion(self.bot.session, regionName, token)
        dfDataRegion = pd.DataFrame(dataRegion)
        dfRegion = map_processing.displayDuplicates(dfDataRegion)

        if len(dfRegion) == 0:
            mbed = discord.Embed(
                color=discord.Colour.dark_red(),
                description = cleandoc(f"""
                    "{regionName}" does not correspond with any of our labeled regions.
                    It is possible that we just need to add it. Please let us know if so!
                """),
            )

            return await ctx.send(embed=mbed)


        if len(dfRegion) < 30:
            regionTrueName, region_id = map_processing.Autofill(dfRegion, regionName)

            msg = cleandoc(f"""```diff
                Input: {regionName}
                Selection From: {', '.join(str(elem) for elem in dfRegion['region_name'].values)}
                Selected: {regionTrueName}
            ```""")
        else:
            msg = "```diff\n- More than 30 Regions selected. Please refine your search.```"

        await ctx.send(msg)


    @commands.command(description=help_messages.heatmap_help_msg)
    @commands.check(checks.check_patron)
    async def heatmap(self, ctx, *params):
        if not params:
            return await ctx.send("Please enter a region name or region ID.")

        info_msg = await ctx.send("Getting that map ready for you. One moment, please!")
        await ctx.trigger_typing()

        if params[0].isdigit():
            region_id = params[0]
            regionTrueName = f"Region ID: {region_id}"
            mapWasGenerated = await self.runAnalysis(regionTrueName, region_id)

            if not mapWasGenerated:
                await self.map_command(ctx, params)
                await ctx.send("We have no data on this region yet.")
            else:
                try:
                    await ctx.send(file=discord.File(f'{os.getcwd()}/{region_id}.png'))
                    await map_processing.CleanupImages(region_id)
                except:
                    await ctx.send("Uhhh... I should have a heatmap to give you, but I don't. Please accept this image of a cat fixing our bot instead.")
                    await ctx.send('https://i.redd.it/lel3o4e2hhp11.jpg')

        else:
            regionName = " ".join(params)
            dataRegion = await map_processing.getHeatmapRegion(self.bot.session, regionName, token)
            dfDataRegion = pd.DataFrame(dataRegion)
            dfRegion = map_processing.displayDuplicates(dfDataRegion)

            if not len(dfRegion):
                mbed = discord.Embed(
                    description = cleandoc(f"""
                        "{regionName}" does not correspond with any of our labeled regions.
                        It is possible that we just need to add it. Please let us know if so!
                    """),
                    color=discord.Colour.dark_red()
                )

                return await ctx.send(embed=mbed)

            if len(dfRegion)<30:
                regionTrueName, region_id = map_processing.Autofill(dfRegion, regionName)
                mapWasGenerated = await self.runAnalysis(regionTrueName, region_id)

                if not mapWasGenerated:
                    await self.map_command(ctx, *params)
                    await ctx.send("We have no data on this region yet.")

                else:
                    try:
                        await ctx.send(file=discord.File(f'{os.getcwd()}/{region_id}.png'))
                        await map_processing.CleanupImages(region_id)

                    except:
                        await ctx.send("Uhhh... I should have a heatmap to give you, but I don't. Please accept this image of a cat fixing our bot instead.")
                        await ctx.send('https://i.redd.it/lel3o4e2hhp11.jpg')

            else:
                msg = ">30 Regions selected. Please refine your search."
                await ctx.send(msg)

            await info_msg.delete()


    @commands.command(description=help_messages.map_help_msg)
    async def map(self, ctx, *, joinedParams=None):
        if not joinedParams:
            return await ctx.send("Please enter a region name or region ID.")

        if joinedParams.isdigit():
            region_id = joinedParams
            msg = f"https://raw.githubusercontent.com/Ferrariic/OSRS-Visible-Region-Images/main/Region_Maps/{region_id}.png"

        else:
            regionName = joinedParams
            dataRegion = await map_processing.getHeatmapRegion(self.bot.session, regionName, token)
            dfDataRegion = pd.DataFrame(dataRegion)
            dfRegion = map_processing.displayDuplicates(dfDataRegion)

            if len(dfRegion) == 0:
                mbed = discord.Embed (
                    description = cleandoc(f"""
                        "{regionName}" does not correspond with any of our labeled regions.
                        It is possible that we just need to add it. Please let us know if so!
                    """),
                    color=discord.Colour.dark_red()
                )

                return await ctx.send(embed=mbed)

            if len(dfRegion) < 30:
                regionTrueName, region_id = map_processing.Autofill(dfRegion, regionName)
                msg = f"https://raw.githubusercontent.com/Ferrariic/OSRS-Visible-Region-Images/main/Region_Maps/{region_id}.png"
            else:
                msg = "```diff\n- More than 30 Regions selected. Please refine your search.```"

        await ctx.send(msg)


    # Analysis run for map_processing Heatmap
    async def runAnalysis(self, regionTrueName, region_id):
        region_id = int(region_id)
        data = await map_processing.getHeatmapData(self.bot.session, region_id, token)
        df = pd.DataFrame(data)

        if df.empty:
            return False

        if 'confirmed_ban' in df.columns:
            ban_mask = (df['confirmed_ban'] == 1)
            df_ban = df[ban_mask].copy()
            dfLocalBan = map_processing.convertGlobaltoLocal(region_id, df_ban)

        else:
            dfLocalBan = pd.DataFrame()


        if 'confirmed_player' in df.columns:
            player_mask = (df['confirmed_player'] == 1)
            df_player = df[player_mask].copy()
            dfLocalReal = map_processing.convertGlobaltoLocal(region_id, df_player)

        else:
            dfLocalReal = pd.DataFrame()

        if dfLocalBan.empty or dfLocalReal.empty:
            return False

        map_processing.plotheatmap(dfLocalBan, dfLocalReal, region_id, regionTrueName)
        return True


def setup(bot):
    bot.add_cog(MapCommands(bot))
