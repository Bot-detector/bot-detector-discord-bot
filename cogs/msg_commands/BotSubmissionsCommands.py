import re
from inspect import cleandoc

import pandas as pd
import utils.sql as sql
from discord.ext import commands
import discord

import help_messages
from utils import check_allowed_channel, CommonCog


class BotSubmissionsCommands(CommonCog, name="Bot Submissions Commands"):
    cog_check = check_allowed_channel

    @commands.command(description=help_messages.list_help_msg)
    async def list(self, ctx):
        msg = cleandoc("""
            Please send a link to a Pastebin URL containing your name list.
            Example: !submit https://pastebin.com/iw8MmUzg
            ___________
            Acceptable Formatting:
            Player 1
            Player 2
            Player 3
            Player 4
            Player 5
            ___________
            Pastebin Settings:
            Syntax Highlighting: None
            Paste Expiration: 1 Day
            Paste Exposure: Public
            Folder: No Folder Selected
            Password: {leave blank - no password needed}
            Paste Name / Title: {Include your Label Here}
        """)

        await ctx.author.send(msg)


    @commands.command(description=help_messages.submit_help_msg)
    async def submit(self, ctx, paste_url):

        sqlLabelID = "SELECT ID FROM `labels_submitted` WHERE Label = %s"
        sqlPlayerID = "SELECT ID FROM `players_submitted` WHERE Players = %s"
        sqlLabelInsert = "INSERT IGNORE `labels_submitted`(`Label`) VALUES (%s)"
        sqlPlayersInsert = "INSERT IGNORE `players_submitted`(`Players`) VALUES (%s)"
        sqlInsertPlayerLabel = "INSERT IGNORE `playerlabels_submitted`(`Player_ID`, `Label_ID`) VALUES (%s, %s)"

        domain = re.search('https?:\/\/([A-Za-z_0-9.-]+).*', paste_url).group(1)
        paste_id = re.search('([^\/]+$)', paste_url).group(0)

        print(f"{domain} and {paste_id}")
       
        if "ghostbin.com" in domain:
            #Ghostbin has enabled Cloudflare protections, and we can longer scrape without workarounds.
            await ctx.send("<@&817917814798155866> A new Ghostbin paste for you!")

        elif "pastebin.com" in domain:
            List = sql.get_paste_names(paste_id)
            labelCheck = sql.get_paste_label(paste_id)

            sql.execute_sql(sqlLabelInsert, insert=True, param=[labelCheck])
            sql.InsertPlayers(sqlPlayersInsert, List)

            dfLabelID = pd.DataFrame(sql.execute_sql(sqlLabelID, insert=False, param=[labelCheck]))
            playerID = sql.PlayerID(sqlPlayerID, List)
            sql.InsertPlayerLabel(sqlInsertPlayerLabel, playerID, dfLabelID)

        else:
            await ctx.reply("We currently only support ghostbin.com and passtebin.com pastes.")
            return


        embed = discord.Embed(
            title="Success!", 
            description="Your submission was received successfully.",
            color=discord.Colour.green()
        )
        embed.set_footer(text="Please note that names submitted via !submit are not attributed to the submitter and will not show up in your !kc totals. Only in-game sightings and flags submitted via the plugin contribute to those stats.")
        await ctx.reply(embed=embed)
        
        
def setup(bot):
    bot.add_cog(BotSubmissionsCommands(bot))
