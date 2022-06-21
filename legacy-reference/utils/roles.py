import bisect
import json
import discord

bot_hunter_roles = {
    1:       {"role_id": 825165287526498314, "role_name": "Bot Hunter I"}, # 1 Ban
    5:       {"role_id": 825165422721499167, "role_name": "Bot Hunter II"}, # 5 Bans
    10:      {"role_id": 825165526262874133, "role_name": "Bot Hunter III"}, # 10 Ban
    25:      {"role_id": 825169068667305995, "role_name": "Bot Hunter IV"}, # 25 Bans
    50:      {"role_id": 825165991503069225, "role_name": "Bot Hunter V"}, # 50 Ban
    100:     {"role_id": 825166170989658112, "role_name": "Bot Hunter VI"}, # 100 Bans
    250:     {"role_id": 825166288321642507, "role_name": "Bot Hunter VII"}, # 250 Ban
    500:     {"role_id": 825166386862489623, "role_name": "Bot Hunter VIII"}, # 500 Bans
    1000:    {"role_id": 825166550947332136, "role_name": "Bot Hunter IX"}, # 1000 Ban
    2500:    {"role_id": 825166673337384990, "role_name": "Bot Hunter X"}, # 2500 Bans
    5000:    {"role_id": 825166781056286751, "role_name": "Bot Hunter XI"}, # 5000 Ban
    10000:   {"role_id": 825167037323673631, "role_name": "Bot Hunter XII"}, # 10000 Bans
    25000:   {"role_id": 825167642184777738, "role_name": "Bot Hunter XIII"}, # 25000 Ban
    50000:   {"role_id": 825167838753849384, "role_name": "Bot Hunter XIV"}, # 50000 Bans
    100000:  {"role_id": 825168089363644427, "role_name": "Bot Hunter XV"}, # 100000 Ban
    250000:  {"role_id": 825168309158281247, "role_name": "Bot Hunter XVI"}, # 250000 Bans
    500000:  {"role_id": 825168632615010371, "role_name": "Bot Hunter XVII"}, # 500000 Ban
    750000:  {"role_id": 825168881059758083, "role_name": "Bot Hunter XVIII"}, # 750000 Bans
    1000000: {"role_id": 825169438835081216, "role_name": 'Bot Hunter XIX'}, # 1000000 Ban
    2000000: {"role_id": 825169641491791902, "role_name": "Bot Hunter XX"} # 2000000 Bans
}


special_roles = {
    "Discord-RSN Linked" : {"role_id": 831196988976529438, "description": "Has linked at least one OSRS account to their Discord ID using the `!link` command. Type `!help link` for more info."},
    "Bot Detective" : {"role_id": 830507560783183888, "description": "Users who scout out emerging bot farms and gather data for analysis. These folks are passionate about stopping botting!"},
    "Quality Tester" : {"role_id": 832866713342050304, "description": "A role for those that run the plugin from our source code to ensure our "\
        +"final releases are up to snuff. A huge thank you to all of the QTs!" \
        +"\n\nIf you are interested in become a Quality Tester please reach out to one of the devs. Alternatively, you can use the `!beta` command for more information."},
    "New Developer" : {"role_id": 837766752166215683, "description": "Developers who are interested in contributing to the project."},
}


#Gets bans from all accounts passed in
async def get_multi_player_bans(session, verifiedPlayers):

    async with session.get(url="https://www.osrsbotdetector.com/api/stats/contributions/", json=json.dumps(verifiedPlayers)) as r:
        if r.status != 200:
            return #TODO Figure out what to do here haha

        js = await r.json()
        return int(js['total']['bans'])



async def get_bot_hunter_role(session, verifiedPlayers, member):
    bans = await get_multi_player_bans(session, verifiedPlayers)

    if bans == 0:
        return False, 0, 1 #No rank just yet
    elif bans < 5:
        new_role = discord.utils.find(lambda r: r.id == bot_hunter_roles[1]["role_id"], member.guild.roles)
        next_role_amount = 5
    else:
        kc_amounts = list(bot_hunter_roles.keys())
        kc_placement = bisect.bisect(kc_amounts, bans)

        if kc_amounts[kc_placement] == bans:
            role_key = kc_amounts[kc_placement]
        elif kc_amounts[kc_placement + 1] == bans:
            role_key = kc_amounts[kc_placement + 1]
        else:
            role_key = kc_amounts[kc_placement - 1]

        new_role = discord.utils.find(lambda r: r.id == bot_hunter_roles[role_key]["role_id"], member.guild.roles)
        next_role_amount = kc_amounts[kc_placement]

    return new_role, bans, next_role_amount


async def remove_old_roles(member):
    old_roles = member.roles

    for role in old_roles:
        if 'Bot Hunter' in role.name:
            to_remove = discord.utils.find(lambda r: role.name in r.name, member.roles)
            await member.remove_roles(to_remove)
