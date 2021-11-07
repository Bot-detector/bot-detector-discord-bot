from inspect import cleandoc as clean

###########################
# Fun Commands
###########################

poke_help_msg = "Not sure if the bot is alive? Give it a poke!"

meow_help_msg = "Displays a random image of a cat. :3"

woof_help_msg = "Displays a random dog image."

birb_help_msg = "Display a small friend of the avarian variety for you to cherish."

bunny_help_msg = "A silly rabbit .gif, but for you!"

###########################
# Info Commands
###########################

utc_help_msg = "Shows the current UTC datestring. Mostly for use by developers."

rules_help_msg = "Shows a link to our rules channel. Be sure to read them carefully!"

website_help_msg = "Shows a link to our website."

beta_help_msg = clean("""
    Don't want to wait for official releases to come out for new features? Want to help us test the plugin? This guide will teach you how to
    build the plugin for our source code."
""")

patreon_help_msg = "Shows a link to ur Patreon page. Patrons get access to exclusuive channels and the !heatmap command."

github_help_msg = "Provides a link to our organization's Github page that has a list of all of our repositories. Feel free to check out the code!"

invite_help_msg = "Places an invite link to the Discord server in the chat. Feel free to invite your friends!"

issues_help_msg = "Having an issue with the plugin? !issues puts a link to #plugin-issues into the chat, where you can let us know."

roles_help_msg = "Lists the Discord roles available to our users."

###########################
# Bot Submissions Commands
###########################

list_help_msg = clean("""
    This will tell the bot to send you a DM detailing how to submit
    a list of player names for review via Pastebin.com.
    This assists us in developing new bot labels.
""")

submit_help_msg = clean("""
    Usage: !submit <pastebin URL> Submit a list of names with a label for us to review.
    Use the !list command for formatting rules.
""")

###########################
# Map Commands
###########################

region_help_msg = clean("""
    Usage: !region <region name> Searches for region names that contain the provided region name substring
    and returns a list of matching regions. If the search returns more than 30 entries then you will need to refine your search.
""")

map_help_msg = "Usage: !map <region name OR region ID> Displays a photo of the region requested in the command."

heatmap_help_msg = clean("""
    PATREON ONLY - Usage: !heatmap <region name> Displays a map of a region with an overlay that shows the intensities of
    confirmed bots (warm colors) and confirmed players (cool colors) seen in that region. Must be ran in #patreon-chat-channel
""")

coords_help_msg = "EXPERIMENTAL - Usage: !coords <x y z zoom> More details to come."


###########################
# Player Stats Commands
###########################

lookup_help_msg = "Usage: !lookup <player name> Places a table in chat show the hiscores entries for a player."

kc_help_msg = clean("""
    Usage: !kc <player name> Shows how many sightings and flags a player has submitted through our plugin
    and home many possible and confirmed bans have resulted from those uploads.
""")

rankup_help_msg = clean("""
    Have you been an absolute reaper of bots, and you want your Discord role to reflect it? Calling this command will
    tell the bot to try and update your Bot Hunter Role. You MUST have used !link to pair at least one OSRS account with your Discord
    ID. The bot will tally up your KC from all accounts you have linked. This command will also give you the Verified RSN role.
""")

predict_help_msg = clean("""
    Usage: !predict <player name> Runs the player through our machine learning model
    and displays the classifications the ML model assigns to the player. Note that any line with a confidence below 75% is insignificant.
""")

excelban_help_msg = clean("""
    You must link your Discord account with an OSRS account in order to use this command. You will only be able
    to retrieve exports for accounts you have linked to with !link. Exports the breakdown of player sightings you have submitted
    which have resulted in bans in an .xlsx file format.
""")

equip_help_msg = clean("""
    Shows the last equipment layout a player was seen in.
""")

xpgain_help_msg = clean("""
    Displays the latest skill xp and boss/minigame completion count difference between our second-to-latest and latest 
    hiscores scrapes for the specified user. We scrape the hiscores once daily for every player in our database that has not been banned.
    The duration is the amount of time between the last two scrapes. The duration will be "Insufficient data" if we only have one day's worth
    of scrape data for a player.
""")

###########################
# Project Stats Commands
###########################

stats_help_msg = "Displays the project-wide flagging statistics. Also shows total active users in the last 7 days."


###########################
# RSN Link Commands
###########################

link_help_msg = clean("""
    Usage: !link <your OSRS name> Allows you to pair an OSRS account with your Discord ID. This will allow for auto-rank assignment in the future.
    Currently, linking allows you to vote on predictions with reactions in #bot-detector-commands and receive your ban breakdowns with !excelban.


    YOU DO NOT NEED TO !LINK YOUR OSRS ACCOUNT FOR YOUR !KC TO INCREASE. For that you need to have Anonymous Mode disabled on your plugin
""")

linked_help_msg = "The bot will DM you which OSRS accounts are linked to your Discord ID."

verify_help_msg = "Usage: !verify <player name> Shows the verification status of a player."
