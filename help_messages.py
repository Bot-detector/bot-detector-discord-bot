###########################
# Fun Commands
###########################

poke_help_msg = f"Not sure if the bot is alive? Give it a poke!"

meow_help_msg = f"Displays a random image of a cat. :3"

woof_help_msg = f"Displays a random dog image."

birb_help_msg = f"Display a small friend of the avarian variety for you to cherish."

bunny_help_msg = f"A silly rabbit .gif, but for you!"


###########################
# Info Commands
###########################

utc_help_msg = f"Shows the current UTC datestring. Mostly for use by developers."

rules_help_msg = f"Shows a link to our rules channel. Be sure to read them carefully!"

website_help_msg = f"Shows a link to our website."

beta_help_msg = f"Don't want to wait for official releases to come out for new features? Want to help us test the plugin? This guide will teach you how to " \
    + "build the plugin for our source code."

patreon_help_msg = f"Shows a link to ur Patreon page. Patrons get access to exclusuive channels and the !heatmap command."

github_help_msg = f"Usage: !github < core | plugin | discord | website > Shows a link to one of our repositories depending on which repo name you enter."

invite_help_msg = f"Places an invite link to the Discord server in the chat. Feel free to invite your friends!"

issues_help_msg = f"Having an issue with the plugin? !issues puts a link to #plugin-issues into the chat, where you can let us know."

roles_help_msg = f"Lists the Discord roles available to our users."

labels_help_msg = f"Lists the player labels that the ML model currently will try to identify players as. These will change over time."

###########################
# Bot Submissions Commands
###########################

list_help_msg = f"This will tell the bot to send you a DM detailing how to submit " \
    + "a list of player names for review via Pastebin.com.\nThis assists us in developing new bot labels."

submit_help_msg = f"Usage: !submit <pastebin URL> Submit a list of names with a label for us to review. " \
    + "Use the !list command for formatting rules."


###########################
# Map Commands
###########################

region_help_msg = f"Usage: !region <region name> Searches for region names that contain the provided region name substring " \
    + "and returns a list of matching regions. If the search returns more than 30 entries then you will need to refine your search."

map_help_msg = f"Usage: !map <region name OR region ID> Displays a photo of the region requested in the command."

heatmap_help_msg = f"PATREON ONLY - Usage: !heatmap <region name> Displays a map of a region with an overlay that shows the intensities of " \
    + "confirmed bots (warm colors) and confirmed players (cool colors) seen in that region. Must be ran in #patreon-chat-channel"

coords_help_msg = f"EXPERIMENTAL - Usage: !coords <x y z zoom> More details to come."


###########################
# Player Stats Commands
###########################

lookup_help_msg = f"Usage: !lookup <player name> Places a table in chat show the hiscores entries for a player."

kc_help_msg = f"Usage: !kc <player name> Shows how many reports (passive and manual) a player has submitted through our plugin " \
    + "and home many possible and confirmed bans have resulted from those reports."

rankup_help_msg = f"Have you been an absolute reaper of bots, and you want your Discord role to reflect it? Calling this command will " \
    + "tell the bot to try and update your Bot Hunter Role. You MUST have used !link to pair at least one OSRS account with your Discord " \
    + "ID. The bot will tally up your KC from all accounts you have linked. This command will also give you the Verified RSN role."

predict_help_msg = f"Usage: !predict <player name> Runs the player through our machine learning model " \
    + "and displays the classifications the ML model assigns to the player. Note that any line with a confidence below "\
    + "75% is insignificant."

excelban_help_msg = f"You must link your Discord account with an OSRS account in order to use this command. You will only be able "\
    + "to retrieve exports for accounts you have linked to with !link. Exports the breakdown of player sightings you have submitted "\
    + "which have resulted in bans in an .xlsx file format."

csvban_help_msg = f"You must link your Discord account with an OSRS account in order to use this command. You will only be able "\
    + "to retrieve exports for accounts you have linked to with !link. Exports the breakdown of player sightings you have submitted "\
    + "which have resulted in bans in a .csv file format."


###########################
# Project Stats Commands
###########################

stats_help_msg = f"Displays the project-wide reporting statistics. Also shows total active users in the last 7 days."


###########################
# RSN Link Commands
###########################

link_help_msg = f"Usage: !link <your OSRS name> Allows you to pair an OSRS account with your Discord ID. This will allow for auto-rank assignment in the future. " \
    + "Currently, linking allows you to vote on predictions with reactions in #bot-commands and receive your ban breakdowns with !excelban and !csvban. " \
    +"\n\nYOU DO NOT NEED TO !LINK YOUR OSRS ACCOUNT FOR YOUR !KC TO INCREASE. For that you need to have Anonymous Mode disabled on your plugin."

linked_help_msg = f"The bot will DM you which OSRS accounts are linked to your Discord ID."

verify_help_msg = f"Usage: !verify <player name> Shows the verification status of a player."