import asyncio
import logging

import aiohttp

logger = logging.getLogger(__name__)


class Api:
    def __init__(self, token) -> None:
        self.token = token
        self.url = "https://www.osrsbotdetector.com/dev"
        self.session = aiohttp.ClientSession()

    async def create_player(self, name: str) -> None:
        url = self.url + "/v1/player"
        await self.session.post(url, params={"player_name": name, "token": self.token})

    async def get_player(self, name: str, debug: bool = False) -> dict:
        url = self.url + "/v1/player"
        resp = await self.session.get(
            url,
            params={
                "player_name": name,
                "token": self.token,
                "row_count": 1,
                "page": 1,
            },
        )
        if resp.ok:
            data = await resp.json()
            if not data:
                logger.debug(f"Could not parse: {name=}")
                data = None
            else:
                data = data[0]
        else:
            logger.error(await resp.json())
            data = None
        if debug:
            logger.debug(f"{resp.status=}, {name=}")
        return data
