import asyncio
import logging
from typing import List

import aiohttp
from src import config

logger = logging.getLogger(__name__)


class Api:
    def __init__(self, token, url) -> None:
        self.token = token
        self.url = url
        self.session = aiohttp.ClientSession()

    def _sanitize_params(self, params: dict):
        if params is None:
            return None
        secure = ["token"]
        return {k: "***" if k in secure else v for k, v in params.items()}

    def __sanitize_url(self, string: str, values: list) -> str:
        for v in values:
            string = string.replace(v, "***")
        return string

    async def _webrequest(
        self, url: str, params: dict = None, json: dict = None, type: str = "get"
    ):
        logger.debug(
            f"{type=}, url={self.__sanitize_url(url, [self.token])}, params={self._sanitize_params(params)}"
        )
        # make web request
        if type == "get":
            response = await self.session.get(url, params=params)
        elif type == "post":
            response = await self.session.post(url, json=json, params=params)
        else:
            return None
        # handle response
        if not response.ok:
            logger.error(
                f"{type=}, url={self.__sanitize_url(url,[self.token])}, params={self._sanitize_params(params)}"
            )
            return None

        # parse response
        if type == "get":
            data = await response.json()
        else:
            try:
                data = await response.json()
            except:
                data = None
        return data

    async def create_player(self, name: str) -> None:
        url = self.url + "/v1/player"
        await self.session.post(url, params={"player_name": name, "token": self.token})

    async def get_player(self, name: str, debug: bool = False) -> dict:
        url = self.url + "/v1/player"
        params = {
            "player_name": name,
            "token": self.token,
            "row_count": 1,
            "page": 1,
        }
        data = await self._webrequest(url, type="get", params=params)
        if data:
            data = data[0]
        return data

    # TODO: API design
    async def get_discord_player(self, runescape_name: str) -> List[dict]:
        url = (
            self.url
            + f"/discord/verify/player_rsn_discord_account_status/{self.token}/{runescape_name}"
        )
        data = await self._webrequest(url, type="get")
        return data

    # TODO: API design
    async def post_discord_code(
        self, discord_id: str, player_name: int, code: str
    ) -> List[dict]:
        url = self.url + f"/discord/verify/insert_player_dpc/{self.token}"
        data = {"discord_id": discord_id, "player_name": player_name, "code": code}
        await self._webrequest(url, type="post", json=data)

    # TODO: API design
    async def get_discord_links(self, discord_id: str) -> List[dict]:
        url = self.url + f"/discord/get_linked_accounts/{self.token}/{discord_id}"
        data = await self._webrequest(url, type="get")
        return data

    # TODO: API design
    async def get_project_stats(self) -> List[dict]:
        url = self.url + "/site/dashboard/projectstats"
        data = await self._webrequest(url, type="get")
        return data

    async def get_hiscore_latest(self, player_id: int) -> List[dict]:
        url = self.url + "/v1/hiscore/Latest"
        params = {"player_id": player_id, "token": self.token}
        data = await self._webrequest(url, type="get", params=params)
        return data

    async def get_contributions(self, players, patreon: bool = False):
        url = self.url + "/stats/contributions"
        params = dict()
        if patreon:
            params = {"token": self.token}
        data = await self._webrequest(url, json=players, type="post", params=params)
        return data

    async def get_prediction(self, player_name):
        url = self.url + "/v1/prediction"
        params = {"name": player_name}
        data = await self._webrequest(url, type="get", params=params)
        return data

    async def get_heatmap_region(self, region_name):
        url = self.url + f"/discord/region/{self.token}"
        params = {"region_name": region_name}
        data = await self._webrequest(url, type="post", json=params)
        return data

    async def get_heatmap_data(self, region_id):
        url = self.url + f"/discord/heatmap/{self.token}"
        params = {"region_id": region_id}
        data = await self._webrequest(url, type="post", json=params)
        return data

    async def get_latest_sighting(self, name: str):
        url = self.url + f"/discord/get_latest_sighting/{self.token}"
        params = {"player_name": name}
        data = await self._webrequest(url, type="post", json=params)
        return data

    async def get_xp_gainz(self, name: str):
        url = self.url + f"/discord/get_xp_gains/{self.token}"
        print(url)
        params = {"player_name": name}
        data = await self._webrequest(url, type="post", json=params)
        return data
