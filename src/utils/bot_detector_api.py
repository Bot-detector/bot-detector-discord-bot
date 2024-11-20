import asyncio
import logging
from typing import List

import aiohttp
from src import config
from src.utils.string_processing import to_jagex_name

logger = logging.getLogger(__name__)


class Api:
    """
    A simple class for making web requests to the bot detector plugin using the aiohttp library.

    Parameters
    ----------
    token : str
        An authentication token to be used in the web request.
    url : str
        The base URL to be used in the web request.

    Attributes
    ----------
    token : str
        An authentication token to be used in the web request.
    url : str
        The base URL to be used in the web request.
    session : aiohttp.ClientSession
        A session to be used for making web requests.
    """

    def __init__(self, token, url) -> None:
        """
        Initialize the `Api` object.

        Parameters
        ----------
        token : str
            An authentication token to be used in the web request.
        url : str
            The base URL to be used in the web request.

        Returns
        -------
        None
        """
        self.token = token
        self.url = url
        self.session = aiohttp.ClientSession()

    def _sanitize_params(self, params: dict):
        """
        Sanitize the parameters in the given dictionary, replacing sensitive values with '***'.

        Parameters
        ----------
        params : dict
            A dictionary of parameters to be sanitized.

        Returns
        -------
        dict
            The sanitized dictionary of parameters.
        """
        if params is None:
            return None
        secure = ["token"]
        return {k: "***" if k in secure else v for k, v in params.items()}

    def _sanitize_url(self, string: str, values: list) -> str:
        """
        Sanitize the given URL, replacing sensitive values with '***'.

        This method is private and should not be called directly.

        Parameters
        ----------
        string : str
            The URL to be sanitized.
        values : list
            A list of sensitive values to be replaced in the URL.

        Returns
        -------
        str
            The sanitized URL.
        """
        for v in values:
            string = string.replace(v, "***")
        return string

    async def _webrequest(
        self,
        url: str,
        params: dict = None,
        json: dict = None,
        type: str = "get",
        debug: bool = True,
        repeat: int = 0,
    ):
        """
        Make a web request with the given parameters.

        This method is private and should not be called directly.

        Parameters
        ----------
        url : str
            The URL to make the web request to.
        params : dict, optional
            A dictionary of parameters to be passed in the web request (default is None).
        json : dict, optional
            A dictionary of JSON data to be passed in the web request (default is None).
        type : str, optional
            The type of web request to make, either "get" or "post" (default is "get").
        debug : bool, optional
            A flag indicating whether to print debug information (default is True).
        repeat : int, optional
            The number of times the web request should be repeated in case of a server error (default is 0).

        Returns
        -------
        dict
            The JSON data returned by the web request, or None if an error occurred.
        """
        max_repeat = 3
        debug_text = f"{type=}, url={self._sanitize_url(url,[self.token])}, params={self._sanitize_params(params)}, json={json}"
        if debug:
            logger.debug(debug_text)

        # make web request
        match type:
            case "get":
                response = await self.session.get(url, params=params)
            case "post":
                response = await self.session.post(url, json=json, params=params)
            case _:
                logger.error(
                    {
                        "error": f"invalid type: received {type} expected (get, post)",
                        "debug": debug_text,
                    }
                )
                return None

        # handle response
        if response.status >= 500:
            if repeat >= max_repeat:
                logger.error(
                    {
                        "error": await response.text(),
                        "debug": debug_text,
                        "status": response.status,
                    }
                )
                return None
            repeat += 1
            data = await self._webrequest(url, params, json, type, debug, repeat)
            return data
        elif not response.ok:
            logger.error(
                {
                    "error": await response.text(),
                    "debug": debug_text,
                    "status": response.status,
                }
            )
            return None

        # parse response
        try:
            data = await response.json()
        except Exception as e:
            if type == "get":
                logger.error(
                    {
                        "error": str(e),
                        "error-text": await response.text(),
                        "debug": debug_text,
                    }
                )
            return None
        logger.debug(data)
        return data

    async def create_player(self, name: str, debug: bool = False) -> None:
        """
        Create a new player.

        This method calls the API endpoint for creating a new player.

        Args:
            name (str): The name of the player to create.
            debug (bool, optional): Whether to enable debugging for the request.
                Defaults to False.

        Returns:
            None
        """
        url = self.url + "/v1/player"
        name = to_jagex_name(name=name)
        data = await self._webrequest(
            url,
            type="post",
            params={"player_name": name, "token": self.token},
            debug=debug,
        )
        return data

    async def get_player(self, name: str, debug: bool = False) -> dict:
        """
        Get a player by name.

        This method calls the API endpoint for getting a player by name and returns
        the player data as a dictionary.

        Args:
            name (str): The name of the player to get.
            debug (bool, optional): Whether to enable debugging for the request.
                Defaults to False.

        Returns:
            dict: The player data, or an empty dictionary if the player was not found.
        """
        url = self.url + "/v1/player"
        params = {
            "player_name": to_jagex_name(name=name),
            "token": self.token,
            "row_count": 1,
            "page": 1,
        }
        data = await self._webrequest(url, type="get", params=params, debug=debug)
        if data:
            data = data[0]
        return data

    # TODO: API design
    async def get_discord_player(self, name: str) -> List[dict]:
        """
        Get a player's Discord account by their RuneScape name.

        This method calls the API endpoint for getting a player's Discord account
        by their RuneScape name, and returns a list of dictionaries containing the
        player's Discord account information.

        Args:
            name (str): The RuneScape name of the player to get.

        Returns:
            List[dict]: A list of dictionaries containing the player's Discord
                account information, or an empty list if the player was not found.
        """
        name = to_jagex_name(name=name)
        url = (
            self.url
            + f"/discord/verify/player_rsn_discord_account_status/{self.token}/{name}"
        )
        data = await self._webrequest(url, type="get")
        return data

    # TODO: API design
    async def post_discord_code(
        self, discord_id: str, name: int, code: str
    ) -> List[dict]:
        """
        Post a Discord verification code for a player.

        This method calls the API endpoint for posting a Discord verification code
        for a player.

        Args:
            discord_id (str): The Discord ID of the player to verify.
            player_name (int): The RuneScape name of the player to verify.
            code (str): The Discord verification code.

        Returns:
            None
        """
        name = to_jagex_name(name=name)
        url = self.url + f"/discord/verify/insert_player_dpc/{self.token}"
        data = {"discord_id": discord_id, "player_name": name, "code": code}
        await self._webrequest(url, type="post", json=data)

    # TODO: API design
    async def get_discord_links(self, discord_id: str) -> List[dict]:
        """
        Get the RuneScape accounts linked to a Discord account.

        This method calls the API endpoint for getting the RuneScape accounts
        linked to a Discord account, and returns a list of dictionaries containing
        the linked RuneScape account information.

        Args:
            discord_id (str): The Discord ID of the player to get.

        Returns:
            List[dict]: A list of dictionaries containing the linked RuneScape
                account information, or an empty list if no RuneScape accounts
                were found.
        """
        url = self.url + f"/discord/get_linked_accounts/{self.token}/{discord_id}"
        data = await self._webrequest(url, type="get")
        return data

    # TODO: API design
    async def get_project_stats(self) -> List[dict]:
        """
        Get project statistics.

        This method calls the API endpoint for getting project statistics,
        and returns a list of dictionaries containing the statistics data.

        Returns:
            List[dict]: A list of dictionaries containing the project statistics.
        """
        url = self.url + "/site/dashboard/projectstats"
        data = await self._webrequest(url, type="get")
        return data

    async def get_hiscore_latest(self, player_id: int) -> List[dict]:
        """
        Get the latest hiscore data for a player.

        This method calls the API endpoint for getting the latest hiscore data
        for a player, and returns a list of dictionaries containing the data.

        Args:
            player_id (int): The ID of the player to get.

        Returns:
            List[dict]: A list of dictionaries containing the player's latest
                hiscore data.
        """
        url = self.url + "/v1/hiscore/Latest"
        params = {"player_id": player_id, "token": self.token}
        data = await self._webrequest(url, type="get", params=params)
        return data

    async def get_contributions(self, players, patreon: bool = False):
        """
        Get contribution data for a player or list of players.

        This method calls the API endpoint for getting contribution data for
        a player or list of players, and returns the data as a dictionary.

        Args:
            players (int or list): The player(s) to get contribution data for.
                Can be a single player ID or a list of player IDs.
            patreon (bool, optional): Whether to include Patreon contributions
                in the data. Defaults to False.

        Returns:
            dict: The contribution data for the player(s), or an empty dictionary
                if the player(s) were not found.
        """
        url = self.url + "/stats/contributions/"
        params = dict()
        if patreon:
            params = {"token": self.token}
        data = await self._webrequest(url, json=players, type="post", params=params)
        return data

    async def get_prediction(self, player_name: str, breakdown: bool = True) -> dict:
        """
        Get a player's skill predictions.

        This method calls the API endpoint for getting a player's skill predictions,
        and returns the data as a dictionary.

        Args:
            player_name (str): The name of the player to get predictions for.
            breakdown (bool, optional): Whether to include a breakdown of the
                predicted skill levels. Defaults to True.

        Returns:
            dict: The player's skill predictions, or an empty dictionary if the
                player was not found.
        """
        url = self.url + "/v1/prediction"
        player_name = to_jagex_name(name=player_name)
        params = {"name": player_name, "breakdown": int(breakdown)}
        data = await self._webrequest(url, type="get", params=params)
        return data

    async def get_heatmap_region(self, region_name: str):
        """
        Get the heatmap data for a region.

        This method calls the API endpoint for getting the heatmap data for
        a region, and returns the data as a dictionary.

        Args:
            region_name (str): The name of the region to get heatmap data for.

        Returns:
            dict: The heatmap data for the region, or an empty dictionary if the region was not found.
        """
        url = self.url + f"/discord/region/{self.token}"
        params = {"region_name": region_name}
        data = await self._webrequest(url, type="post", json=params)
        return data

    async def get_heatmap_data(self, region_id: int):
        """
        Get the heatmap data for a region.

        This method calls the API endpoint for getting the heatmap data for
        a region, and returns the data as a dictionary.

        Args:
            region_id (int): The ID of the region to get heatmap data for.

        Returns:
            dict: The heatmap data for the region, or an empty dictionary if the region was not found.
        """
        url = self.url + f"/discord/heatmap/{self.token}"
        params = {"region_id": region_id}
        data = await self._webrequest(url, type="post", json=params)
        return data

    async def get_latest_sighting(self, name: str):
        """
        Get the latest sighting data for a player.

        This method calls the API endpoint for getting the latest sighting data
        for a player, and returns the data as a dictionary.

        Args:
            name (str): The name of the player to get sighting data for.

        Returns:
            dict: The latest sighting data for the player, or an empty dictionary
                if the player was not found.
        """
        url = self.url + f"/discord/get_latest_sighting/{self.token}"
        params = {"player_name": to_jagex_name(name=name)}
        data = await self._webrequest(url, type="post", json=params)
        return data

    async def get_xp_gainz(self, name: str):
        """
        Get the XP gains for a player.

        This method calls the API endpoint for getting the XP gains for
        a player, and returns the data as a dictionary.

        Args:
            name (str): The name of the player to get XP gains for.

        Returns:
            dict: The XP gains for the player, or an empty dictionary
                if the player was not found.
        """
        url = self.url + f"/discord/get_xp_gains/{self.token}"
        params = {"player_name": to_jagex_name(name=name)}
        data = await self._webrequest(url, type="post", json=params)
        return data

    async def get_player_report_score(self, names: list[str]) -> list[dict]:
        url = "https://api-v2.prd.osrsbotdetector.com/v2/player/report/score"
        params = {"name": names}
        data = await self._webrequest(url, type="get", params=params)
        return data

    async def get_player_feedback_score(self, names: list[str]) -> list[dict]:
        url = "https://api-v2.prd.osrsbotdetector.com/v2/player/feedback/score"
        params = {"name": names}
        data = await self._webrequest(url, type="get", params=params)
        return data