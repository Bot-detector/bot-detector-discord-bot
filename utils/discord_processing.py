from typing import Optional, Dict

import aiohttp

BASE_URL = 'https://www.osrsbotdetector.com/api'

async def get_player_verification_full_status(session: aiohttp.ClientSession, playerName: str, token: str) -> Optional[dict]:
    url = f'{BASE_URL}/discord/verify/player_rsn_discord_account_status/{token}/{playerName}'

    async with session.get(url) as r:
        if r.status == 200:
            data = await r.json()

    try:
        return data
    except:
        return None


async def get_playerid_verification(session: aiohttp.ClientSession, playerName, token):
    url = f'{BASE_URL}/discord/verify/playerid/{token}/{playerName}'

    async with session.get(url) as r:
        if r.status == 200:
            playerIDverif = await r.json()

    try:
        return playerIDverif[0]
    except:
        return None


async def get_verified_player_info(session: aiohttp.ClientSession, playerName, token):
    url = f'{BASE_URL}/discord/verify/verified_player_info/{token}/{playerName}'

    async with session.get(url) as r:
        if r.status == 200:
            vplayerinfo = await r.json()

    return vplayerinfo[0]


async def post_discord_player_info(session: aiohttp.ClientSession, discord_id, player_id, code, token):
    id = player_id['id']
    url = f'{BASE_URL}/discord/verify/insert_player_dpc/{token}/{discord_id}/{id}/{code}'

    async with session.post(url) as r:
        return await r.json() if r.status == 200 else {"error":f"Failed: {r.status} error"}


async def get_linked_accounts(session: aiohttp.ClientSession, discord_id: str, token: str) -> Optional[dict]:
    url = f'{BASE_URL}/discord/get_linked_accounts/{token}/{discord_id}'

    async with session.get(url) as r:
        if r.status == 200:
            linkedAccounts = await r.json()

    try:
        return linkedAccounts
    except:
        return None

async def get_discords_ids_with_links(session: aiohttp.ClientSession, token):
    url = f'{BASE_URL}/discord/get_all_linked_ids/{token}'

    async with session.get(url) as r:
        if r.status == 200:
            discordIDList = await r.json()

    return discordIDList

async def get_player_labels(session: aiohttp.ClientSession):
    url = f'{BASE_URL}/labels/get_player_labels'

    async with session.get(url) as r:
        if r.status == 200:
            labels = await r.json()

    try:
        return labels
    except:
        return None
