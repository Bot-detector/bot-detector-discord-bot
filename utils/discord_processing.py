import aiohttp

BASE_URL = 'https://www.osrsbotdetector.com/dev'

async def get_player_verification_full_status(playerName, token):

    url = f'{BASE_URL}/discord/verify/player_rsn_discord_account_status/{token}/{playerName}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                data = await r.json()

    

    try:
        return data[0]
    except:
        return None

async def get_playerid_verification(playerName, token):

    url = f'{BASE_URL}/discord/verify/playerid/{token}/{playerName}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                playerIDverif = await r.json()

    print(playerIDverif)
    
    try:
        return playerIDverif[0]
    except:
        return None

async def get_verified_player_info(playerName, token):

    url = f'{BASE_URL}/discord/verify/verified_player_info/{token}/{playerName}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                vplayerinfo = await r.json()

    return vplayerinfo[0]

async def post_discord_player_info(discord_id, player_id, code, token):

    id = player_id['id']

    url = f'{BASE_URL}/discord/verify/insert_player_dpc/{token}/{discord_id}/{id}/{code}'

    async with aiohttp.ClientSession() as session:
        async with session.post(url) as r:
            return await r.json() if r.status == 200 else {"error":f"Failed: {r.status} error"}