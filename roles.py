import discord
import aiohttp
import bisect

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
    "verified_rsn" : 831196988976529438
}


#Gets bans from all accounts passed in
async def get_multi_player_contributions(verifiedPlayers):
    
    totalBans = 0
    totalPossibleBans = 0
    totalReports = 0

    for player in verifiedPlayers:
        playerName = player["name"]

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.osrsbotdetector.com/api/stats/contributions/{playerName}") as r:
                if r.status == 200:
                    js = await r.json()
                    totalBans += int(js['bans'])
                    totalPossibleBans += int(js['possible_bans'])
                    totalReports += int(js['reports'])

    return totalBans, totalPossibleBans, totalReports


async def get_bot_hunter_role(verifiedPlayers, member):

    contributions = await get_multi_player_contributions(verifiedPlayers)
    bans = contributions[0]

    if(bans == 0):
        return False #No rank just yet
    elif(bans == 1):
        return discord.utils.find(lambda r: r.id == bot_hunter_roles[1]["role_id"], member.guild.roles)
    else:
        kc_amounts = list(bot_hunter_roles.keys())
        kc_placement = bisect.bisect(kc_amounts, bans)

        if kc_amounts[kc_placement] == bans:
            role_key = kc_amounts[kc_placement]
        elif kc_amounts[kc_placement + 1] == bans:
            role_key = kc_amounts[kc_placement + 1]
        else:
            role_key = kc_amounts[kc_placement - 1]

        return discord.utils.find(lambda r: r.id == bot_hunter_roles[role_key]["role_id"], member.guild.roles)


async def remove_old_roles(member):

    old_roles = member.roles

    for role in old_roles:
        if 'Bot Hunter' in role.name:
            to_remove = discord.utils.find(lambda r: role.name in r.name, member.roles)
            await member.remove_roles(to_remove)
