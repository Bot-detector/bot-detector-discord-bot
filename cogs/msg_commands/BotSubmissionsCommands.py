import os
from inspect import cleandoc

import pandas as pd
import utils.sql as sql
from discord.ext import commands

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
        errors = "No Errors"

        sqlLabelID = "SELECT ID FROM `labels_submitted` WHERE Label = %s"
        sqlPlayerID = "SELECT ID FROM `players_submitted` WHERE Players = %s"
        sqlLabelInsert = "INSERT IGNORE `labels_submitted`(`Label`) VALUES (%s)"
        sqlPlayersInsert = "INSERT IGNORE `players_submitted`(`Players`) VALUES (%s)"
        sqlInsertPlayerLabel = "INSERT IGNORE `playerlabels_submitted`(`Player_ID`, `Label_ID`) VALUES (%s, %s)"

        try:
            paste_soup = sql.get_paste_data(paste_url)
            List = sql.get_paste_names(paste_soup)
            labelCheck = sql.get_paste_label(paste_soup)
            sql.execute_sql(sqlLabelInsert, insert=True, param=[labelCheck])
            sql.InsertPlayers(sqlPlayersInsert, List)
            dfLabelID = pd.DataFrame(sql.execute_sql(sqlLabelID, insert=False, param=[labelCheck]))
            playerID = sql.PlayerID(sqlPlayerID, List)
            sql.InsertPlayerLabel(sqlInsertPlayerLabel, playerID, dfLabelID)

            await ctx.reply("Your list has been received. Thank you!")
        except sql.MissingNamesError:
            await ctx.reply("The Pastebin list you've submitted appears to be empty.")
        except sql.InvalidPasteTitleError:
            await ctx.reply("The Pastebin title submitted was invalid. Please remove any special characters and try again.")
        except Exception as e:
            errors = str(e)
            await ctx.reply("There was an error parsing your list submission.")

        msg = cleandoc(f"""```diff
            Paste Information Submitted
            _____________________
            Link: {paste_url}
            Errors: {errors}
        ```""")

        recipient = await self.bot.fetch_user(int(os.getenv('SUBMIT_RECIPIENT')))
        await recipient.send(msg)
        
        
def setup(bot):
    bot.add_cog(BotSubmissionsCommands(bot))
