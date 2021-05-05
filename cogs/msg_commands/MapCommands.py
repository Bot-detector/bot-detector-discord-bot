from discord.ext.commands import Cog
from discord.ext.commands import command, check

import discord
import os
import pandas as pd
import checks
import help_messages

import utils.string_processing as string_processing
import utils.map_processing as map_processing

from dotenv import load_dotenv
load_dotenv()
token = os.getenv('API_AUTH_TOKEN')

class MapCommands(Cog, name='Map Commands'):

    def __init__(self, bot):
        self.bot = bot

    @command(name="region", description=help_messages.region_help_msg)
    @check(checks.check_allowed_channel)
    async def region_command(self, ctx, *params):
        regionName = string_processing.joinParams(params)
        dataRegion = await map_processing.getHeatmapRegion(regionName, token)
        dfDataRegion = pd.DataFrame(dataRegion)
        dfRegion = map_processing.displayDuplicates(dfDataRegion)

        if len(dfRegion) == 0:
            mbed = discord.Embed (
                description = f"\"{regionName}\" does not correspond with any of our labeled regions." \
                    + " It is possible that we just need to add it. Please let us know if so!",
                color = discord.Colour.dark_red()
            )

            await ctx.channel.send(embed=mbed)
            return
        
        if len(dfRegion) < 30:
            regionTrueName, region_id = map_processing.Autofill(dfRegion, regionName)
            
            msg = "```diff" + "\n" \
                + "+ Input: " + str(regionName) + "\n" \
                + "+ Selection From: " + str(', '.join([str(elem) for elem in dfRegion['region_name'].values])) + "\n" \
                + "+ Selected: " + str(regionTrueName) + "\n" \
                + "```"
        else:
            msg = "```diff" + "\n" \
                + "- More than 30 Regions selected. Please refine your search." + "\n" \
                + "```"
        await ctx.channel.send(msg)


    @command(name="heatmap", description=help_messages.heatmap_help_msg)
    @check(checks.check_patron)
    async def heatmap_command(self, ctx, *params):

        info_msg = await ctx.channel.send("Getting that map ready for you. One moment, please!")

        joinedParams = string_processing.joinParams(params)
        regionName = joinedParams
    
        dataRegion = await map_processing.getHeatmapRegion(regionName, token)
        dfDataRegion = pd.DataFrame(dataRegion)
        dfRegion = map_processing.displayDuplicates(dfDataRegion)

        if len(dfRegion)<30:
            regionTrueName, region_id = map_processing.Autofill(dfRegion, regionName)

            mapWasGenerated = await self.runAnalysis(regionTrueName, region_id)

            if not mapWasGenerated:
                await self.map_command(ctx, params)
                await ctx.channel.send("We have no data on this region yet.")

            else:
                try:
                    await ctx.channel.send(file=discord.File(f'{os.getcwd()}/{region_id}.png'))
                    await map_processing.CleanupImages(region_id)

                except:
                    await ctx.channel.send("Uhhh... I should have a heatmap to give you, but I don't. Please accept this image of a cat fixing our bot instead.")
                    await ctx.channel.send('https://i.redd.it/lel3o4e2hhp11.jpg')

        else:
            msg = ">30 Regions selected. Please refine your search."
            await ctx.channel.send(msg)

        
        await info_msg.delete()


    @command(name="map", description=help_messages.map_help_msg)
    @check(checks.check_allowed_channel)
    async def map_command(self, ctx, *params):

        joinedParams = string_processing.joinParams(params)

        if params[0].isdigit():
            region_id = joinedParams

            msg = str(
                'https://raw.githubusercontent.com/Ferrariic/OSRS-Visible-Region-Images/main/Region_Maps/{}.png'.format(region_id))

        else:
            regionName = joinedParams
            dataRegion = await map_processing.getHeatmapRegion(regionName, token)
            dfDataRegion = pd.DataFrame(dataRegion)
            dfRegion = map_processing.displayDuplicates(dfDataRegion)
        
            if len(dfRegion) < 30:
                regionTrueName, region_id = map_processing.Autofill(dfRegion, regionName)
                msg = str(
                    'https://raw.githubusercontent.com/Ferrariic/OSRS-Visible-Region-Images/main/Region_Maps/{}.png'.format(region_id))
            else:
                msg = "```diff" + "\n" \
                    + "- More than 30 Regions selected. Please refine your search." + "\n" \
                    + "```"
            
        await ctx.channel.send(msg)


    @command(name="coords", description=help_messages.coords_help_msg)
    @check(checks.check_allowed_channel)
    async def coords_command(self, ctx, x, y, z, zoom):

        BASE_URL = "https://raw.githubusercontent.com/Explv/osrs_map_tiles/master/"

        msg = BASE_URL + str(z) + "/" + str(zoom) + "/" + str(y) + "/" + str(x) + ".png"

        await ctx.channel.send(msg)


    # Analysis run for map_processing Heatmap
    async def runAnalysis(self, regionTrueName, region_id):
        region_id = int(region_id)
        data = await map_processing.getHeatmapData(region_id, token)
        df = pd.DataFrame(data)

        if(df.empty):
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
            
        if not dfLocalBan.empty and not dfLocalReal.empty:
            map_processing.plotheatmap(dfLocalBan, dfLocalReal, region_id, regionTrueName)

        else:
            return False


        return True

def setup(bot):
    bot.add_cog(MapCommands(bot))



