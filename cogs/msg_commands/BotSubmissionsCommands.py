from discord.ext.commands import Cog
from discord.ext.commands import command, check

import os
import sql
import checks
import pandas as pd

from dotenv import load_dotenv
load_dotenv()
token = os.getenv('API_AUTH_TOKEN')


class BotSubmissionsCommands(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="list")
    @check(checks.check_allowed_channel)
    async def list_command(self, ctx):
        msg = "Please send a link to a Pastebin URL containing your name list." + "\n" \
            + "Example: !submit https://pastebin.com/iw8MmUzg" + "\n" \
            + "___________" + "\n" \
            + "Acceptable Formatting:" + "\n" \
            + "Player 1" + "\n" \
            + "Player 2" + "\n" \
            + "Player 3" + "\n" \
            + "Player 4" + "\n" \
            + "Player 5" + "\n" \
            + "___________" + "\n" \
            + "Pastebin Settings:" + "\n" \
            + "Syntax Highlighting: None" + "\n" \
            + "Paste Expiration: 1 Day" + "\n" \
            + "Paste Exposure: Public" + "\n" \
            + "Folder: No Folder Selected" + "\n" \
            + "Password: {leave blank - no password needed}" + "\n" \
            + "Paste Name / Title: {Include your Label Here}" + "\n"

        await ctx.author.send(msg)

    @command(name="submit")
    @check(checks.check_allowed_channel)
    async def submit_command(self, ctx, paste_url):
        errors = "No Errors"

        sqlLabelInsert = ('''
        INSERT IGNORE `labels_submitted`(`Label`) VALUES (%s)
        ''')

        sqlPlayersInsert = ('''
        INSERT IGNORE `players_submitted`(`Players`) VALUES (%s)
        ''')

        sqlLabelID = ('''
        SELECT ID FROM `labels_submitted` WHERE Label = %s
        ''')

        sqlPlayerID = ('''
        SELECT ID FROM `players_submitted` WHERE Players = %s
        ''')

        sqlInsertPlayerLabel = ('''
        INSERT IGNORE `playerlabels_submitted`(`Player_ID`, `Label_ID`) VALUES (%s, %s)
        ''')

        try:
            paste_soup = sql.get_paste_data(paste_url)
            List = sql.get_paste_names(paste_soup)
            labelCheck = sql.get_paste_label(paste_soup)
            sql.execute_sql(sqlLabelInsert, insert=True, param=[labelCheck])
            sql.InsertPlayers(sqlPlayersInsert, List)
            dfLabelID = pd.DataFrame(sql.execute_sql(sqlLabelID, insert=False, param=[labelCheck]))
            playerID = sql.PlayerID(sqlPlayerID, List)
            sql.InsertPlayerLabel(sqlInsertPlayerLabel, playerID, dfLabelID)
        except Exception as e:
            errors = str(e)

        msg = "```diff" + "\n" \
            + "Paste Information Submitted" + "\n" \
            + "_____________________" + "\n" \
            + "+ Link: " + str(paste_url) + "\n" \
            + "+ Errors: " + str(errors) + "\n" \
            + "```"

        recipient = self.bot.get_user(int(os.getenv('SUBMIT_RECIPIENT')))
        await recipient.send(msg)


def setup(bot):
    bot.add_cog(BotSubmissionsCommands(bot))