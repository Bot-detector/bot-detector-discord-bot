from typing import Optional, Dict, List

import aiohttp
from discord.errors import HTTPException

BASE_URL = 'https://www.osrsbotdetector.com/api'

async def get_player_verification_full_status(session: aiohttp.ClientSession, player_name: str, token: str):
    url = f'{BASE_URL}/discord/verify/player_rsn_discord_account_status/{token}/{player_name}'

    async with session.get(url) as r:
        if r.status == 200:
            data = await r.json()
            return data

    raise HTTPException(r.status, "Could not grab data.")


#Gets Previous Attempts to Link the Same RSN
async def get_verification_attempts(session: aiohttp.ClientSession, player_name, token):
    url = f'{BASE_URL}/discord/verify/get_verification_attempts/{token}/{player_name}'

    async with session.get(url) as r:
        if r.status == 200:
            attempts = await r.json()
            return attempts

    raise HTTPException(r.status, "Could not grab data.")


async def get_verified_player_info(session: aiohttp.ClientSession, player_name, token):
    url = f'{BASE_URL}/discord/verify/verified_player_info/{token}/{player_name}'

    async with session.get(url) as r:
        if r.status == 200:
            vplayerinfo = await r.json()
            return vplayerinfo[0]

    raise HTTPException(r.status, "Could not grab data.")


async def post_discord_player_info(session: aiohttp.ClientSession, discord_id, player_name, code, token):
    url = f'{BASE_URL}/discord/verify/insert_player_dpc/{token}'

    verify_info = {
        "discord_id": discord_id,
        "player_name": player_name,
        "code": code
    }

    async with session.post(url, json=verify_info) as r:
        return await r.json() if r.status == 200 else {"error":f"Failed: {r.status} error"}


async def get_linked_accounts(session: aiohttp.ClientSession, discord_id: str, token: str) -> Optional[dict]:
    url = f'{BASE_URL}/discord/get_linked_accounts/{token}/{discord_id}'

    async with session.get(url) as r:
        if r.status == 200:
            linkedAccounts = await r.json()
            return linkedAccounts

    raise HTTPException(r.status, "Could not grab data.")


async def get_discords_ids_with_links(session: aiohttp.ClientSession, token):
    url = f'{BASE_URL}/discord/get_all_linked_ids/{token}'

    async with session.get(url) as r:
        if r.status == 200:
            discordIDList = await r.json()
            return discordIDList

    raise HTTPException(r.status, "Could not grab data.")


async def get_discord_id_with_links(session: aiohttp.ClientSession, token):
    url = f'{BASE_URL}/discord/get_all_linked_ids/{token}'

    async with session.get(url) as r:
        if r.status == 200:
            discords_ids = await r.json()
            return discords_ids

    raise HTTPException(r.status, "Could not grab data.")


async def get_latest_runelite_version(session: aiohttp.ClientSession):
    url = "https://static.runelite.net/bootstrap.json"

    async with session.get(url) as r:
        if r.status == 200:
            runelite_data = await r.json()
            version = runelite_data["client"]["version"]
            return version

    raise HTTPException(r.status, "Could not grab data.")


async def get_players(session: aiohttp.ClientSession, player_names, token: str):
    url = f'{BASE_URL}/v1/player/bulk?token={token}'

    req_payload = {
        "player_name":  player_names
    }

    async with session.get(
        url=url,
        json=req_payload
    ) as r:
        if r.status == 200:
            players = await r.json()
            return players
  
    raise HTTPException(r.status, "Could not grab data.")


async def get_latest_feedback(session: aiohttp.ClientSession, token: str, latest_id: int):
    url = f"{BASE_URL}/v1/feedback/?token={token}&since_id={latest_id}&has_text=True"

    async with session.get(url=url) as r:
        if r.status == 200:
            feedback = await r.json()
            return feedback

    raise HTTPException(r.status, "Could not grab data.")


async def get_player(session: aiohttp.ClientSession, token: str, player_id: int):
    url = f"{BASE_URL}/v1/player/?token={token}&player_id={player_id}"

    async with session.get(url=url) as r:
        if r.status == 200:
            player = await r.json()
            return player[0]

    raise HTTPException(r.status, "Could not grab data.")
