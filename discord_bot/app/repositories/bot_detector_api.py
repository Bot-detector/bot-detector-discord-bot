import aiohttp


class BotDetectorAPI:
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the BotDetectorAPI class.

        Args:
            base_url (str): The base URL of the API.
            api_key (str): The API key for authentication.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}  # future proof

    async def _get(self, endpoint: str, params: dict = None) -> dict:
        """
        Send a GET request to the API.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): The URL parameters. Defaults to None.

        Raises:
            ValueError: If the API returns an error status code.

        Returns:
            dict: The JSON response from the API.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}{endpoint}", headers=self.headers, params=params or {}
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise ValueError(
                        f"Failed to fetch {endpoint} with status code {resp.status}"
                    )

    async def _put(self, endpoint: str, params: dict = None) -> dict:
        """
        Send a PUT request to the API.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): The URL parameters. Defaults to None.

        Raises:
            ValueError: If the API returns an error status code.

        Returns:
            dict: The JSON response from the API.
        """
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.base_url}{endpoint}", headers=self.headers, params=params or {}
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise ValueError(
                        f"Failed to update {endpoint} with status code {resp.status}"
                    )

    async def get_player_hiscore_data(
        self, token: str, player_id: int, row_count: int = 10000, page: int = 1
    ) -> dict:
        """
        Select player hiscore data by Player ID.

        Args:
            token (str): The API token.
            player_id (int): The Player ID to search.
            row_count (int, optional): The number of rows to retrieve. Defaults to 10000.
            page (int, optional): The page number to retrieve. Defaults to 1.

        Raises:
            ValueError: If the API returns an error status code.

        Returns:
            dict: The JSON response from the API.
        """
        endpoint = "/v1/hiscore/"
        params = {
            "token": token,
            "player_id": player_id,
            "row_count": row_count,
            "page": page,
        }
        return await self._get(endpoint, params)

    async def get_latest_hiscore_data(self, token: str, player_id: int) -> dict:
        """
        Select the latest hiscore data of a player by Player ID.

        Args:
            token (str): The API token.
            player_id (int): The Player ID to search.

        Raises:
            ValueError: If the API returns an error status code.

        Returns:
            dict: The JSON response from the API.
        """
        endpoint = f"/v1/hiscore/Latest"
        params = {"token": token, "player_id": player_id}
        return await self._get(endpoint, params=params)

    async def get_latest_hiscore_data_by_player_features(
        self,
        token: str,
        row_count: int = 10000,
        page: int = 1,
        possible_ban: int = None,
        confirmed_ban: int = None,
        confirmed_player: int = None,
        label_id: int = None,
        label_jagex: int = None,
    ) -> dict:
        """
        Select the latest hiscore data of multiple players by filtering on the player features.

        Args:
            token (str): API token.
            row_count (int, optional): The number of rows to retrieve (default 10000).
            page (int, optional): The page number to retrieve (default 1).
            possible_ban (int, optional): Possible ban status filter: 1 for true, 0 for false, None for no filter.
            confirmed_ban (int, optional): Confirmed ban status filter: 1 for true, 0 for false, None for no filter.
            confirmed_player (int, optional): Confirmed player status filter: 1 for true, 0 for false, None for no filter.
            label_id (int, optional): The label ID to filter by, None for no filter.
            label_jagex (int, optional): The Jagex label to filter by, None for no filter.

        Raises:
            None

        Returns:
            dict: A dictionary containing the hiscore data for the specified player features.
        """
        endpoint = "/v1/hiscore/Latest/bulk"
        params = {
            "token": token,
            "row_count": row_count,
            "page": page,
            "possible_ban": possible_ban,
            "confirmed_ban": confirmed_ban,
            "confirmed_player": confirmed_player,
            "label_id": label_id,
            "label_jagex": label_jagex,
        }
        return await self._get(endpoint, params=params)

    async def get_account_hiscore_xp_change(
        self, token: str, player_id: int, row_count: int = 10000, page: int = 1
    ):
        """
        Select daily scraped differential in hiscore data by Player ID.

        Args:
            token (str): The BotDetector API token.
            player_id (int): The Player ID.
            row_count (int, optional): The number of rows to retrieve. Defaults to 10000.
            page (int, optional): The page number to retrieve. Defaults to 1.

        Raises:
            ValueError: If the request to BotDetector API's '/v1/hiscore/XPChange' endpoint fails
                with a non-200 status code.

        Returns:
            dict: The response from the BotDetector API's '/v1/hiscore/XPChange' endpoint.
        """
        endpoint = "/v1/hiscore/XPChange"
        params = {
            "token": token,
            "player_id": player_id,
            "row_count": row_count,
            "page": page,
        }
        return await self._get(endpoint, params=params)

    async def get_player_information(
        self,
        token: str,
        player_name: str = None,
        player_id: int = None,
        row_count: int = 10000,
        page: int = 1,
    ) -> dict:
        """Get information about a player.

        Args:
            token (str): Your BotDetector API token.
            player_name (str, optional): The name of the player to search for. Defaults to None.
            player_id (int, optional): The ID of the player to search for. Defaults to None.
            row_count (int, optional): The maximum number of rows to return. Defaults to 10000.
            page (int, optional): The page number to return. Defaults to 1.

        Raises:
            ValueError: If the API returns an error.

        Returns:
            dict: A dictionary containing information about the player.
        """
        endpoint = "/v1/player"
        params = {
            "token": token,
            "player_name": player_name,
            "player_id": player_id,
            "row_count": row_count,
            "page": page,
        }
        response = await self._get(endpoint, params=params)
        return response

    async def get_bulk_player_data(
        self,
        token: str,
        possible_ban: int = None,
        confirmed_ban: int = None,
        confirmed_player: int = None,
        label_id: int = None,
        label_jagex: int = None,
        row_count: int = 10000,
        page: int = 1,
    ):
        """
        Selects bulk player data from the plugin database.

        Args:
            token (str): The API token.
            possible_ban (int, optional): The possible ban status of the players to retrieve. Defaults to None.
            confirmed_ban (int, optional): The confirmed ban status of the players to retrieve. Defaults to None.
            confirmed_player (int, optional): The confirmed player status of the players to retrieve. Defaults to None.
            label_id (int, optional): The label id of the players to retrieve. Defaults to None.
            label_jagex (int, optional): The label jagex of the players to retrieve. Defaults to None.
            row_count (int, optional): The number of rows to retrieve. Defaults to 10000.
            page (int, optional): The page number of the results to retrieve. Defaults to 1.

        Raises:
            ValueError: If the API response indicates an error.

        Returns:
            response (dict): The JSON response from the API.
        """
        endpoint = "/v1/player/bulk"
        params = {
            "token": token,
            "possible_ban": possible_ban,
            "confirmed_ban": confirmed_ban,
            "confirmed_player": confirmed_player,
            "label_id": label_id,
            "label_jagex": label_jagex,
            "row_count": row_count,
            "page": page,
        }
        return await self._get(endpoint, params=params)

    async def get_account_prediction_result(self, name: str, breakdown: bool = False):
        """
        Get account prediction result.

        Args:
            name (str): The name of the player to get the prediction for.
            breakdown (bool, optional): If True, always return breakdown, even if the prediction is Stats_Too_Low (default: False).

        Returns:
            dict: A dictionary containing the prediction data for the player.

        Raises:
            ValueError: If name is not provided or invalid.
        """
        endpoint = "/v1/prediction"
        params = {"name": name, "breakdown": breakdown}
        return await self._get(endpoint, params=params)

    async def get_expired_predictions(self, token: str, limit: int = 5000):
        """
        Get expired predictions.

        Args:
            token (str): Token.
            limit (int, optional): Limit of results to return (default: 5000).

        Returns:
            dict: A dictionary containing the expired prediction data.

        Raises:
            ValueError: If token is not provided or invalid.
        """
        endpoint = "/v1/prediction/data"
        params = {"token": token, "limit": limit}
        return await self._get(endpoint, params=params)

    async def get_predictions_by_player_features(
        self,
        token: str,
        row_count: int = 100000,
        page: int = 1,
        possible_ban: int = None,
        confirmed_ban: int = None,
        confirmed_player: int = None,
        label_id: int = None,
        label_jagex: int = None,
    ):
        """
        Get predictions by player features.

        Args:
            token (str): Token.
            row_count (int, optional): The number of rows to return (default: 10000).
            page (int, optional): The page number to return (default: 1).
            possible_ban (int, optional): Possible ban type to filter results (default: None).
            confirmed_ban (int, optional): Confirmed ban type to filter results (default: None).
            confirmed_player (int, optional): Confirmed player status to filter results (default: None).
            label_id (int, optional): The prediction label to filter results (default: None).
            label_jagex (int, optional): The Jagex label to filter results (default: None).

        Returns:
            dict: A dictionary containing the prediction data for the player.

        Raises:
            ValueError: If token is not provided or invalid.
        """
        endpoint = "/v1/prediction/bulk"
        params = {
            "token": token,
            "row_count": row_count,
            "page": page,
            "possible_ban": possible_ban,
            "confirmed_ban": confirmed_ban,
            "confirmed_player": confirmed_player,
            "label_id": label_id,
            "label_jagex": label_jagex,
        }
        return await self._get(endpoint, params=params)

    async def get_feedback(
        self, token: str, name: str, row_count: int = 5000, page: int = 1
    ):
        """
        Get player feedback for a player.

        Args:
            token (str): Token.
            name (str): Name.
            row_count (int, optional): Row Count (default: 10000).
            page (int, optional): Page (default: 1).

        Returns:
            dict: A dictionary containing the feedback data.

        Raises:
            ValueError: If token is not provided or invalid.
        """
        endpoint = "/v1/feedback/"
        params = {
            "token": token,
            "name": name,
            "row_count": row_count,
            "page": page,
        }
        return await self._get(endpoint, params=params)

    async def get_feedback_count(self, name: str):
        """
        Get feedback count for a player.

        Args:
            name (str): Name.

        Returns:
            dict: A dictionary containing the feedback count data.

        Raises:
            ValueError: If name is not provided or invalid.
        """
        endpoint = "/v1/feedback/count"
        params = {"name": name}
        response = await self._get(endpoint, params=params)
        return response

    async def get_reports(
        self,
        token: str,
        reportedID: int = None,
        reportingID: int = None,
        timestamp: str = None,
        regionID: int = None,
        row_count: int = 10000,
    ) -> dict:
        """
        Returns a dictionary containing a list of reports that match the specified filters.

        Args:
            token (str): A valid BotDetector API token.
            reportedID (int, optional): The ID of the reported user.
            reportingID (int, optional): The ID of the reporting user.
            timestamp (str, optional): A timestamp string in ISO 8601 format representing the
                latest timestamp to retrieve reports from. Defaults to None.
            regionID (int, optional): The ID of the region to filter reports by.
            row_count (int, optional): The maximum number of rows to retrieve. Defaults to 10000.

        Raises:
            ValueError: If any of the arguments are invalid.

        Returns:
            A dictionary containing a list of reports that match the specified filters.
        """
        endpoint = "/v1/report"
        params = {
            "token": token,
            "reportedID": reportedID,
            "reportingID": reportingID,
            "timestamp": timestamp,
            "regionID": regionID,
            "row_count": row_count,
        }
        return await self._get(endpoint, params=params)

    async def update_reports(
        self,
        old_user_id: int,
        new_user_id: int,
        token: str,
    ) -> dict:
        """
        Updates the user ID of all reports that were filed against the specified old user ID.

        Args:
            old_user_id (int): The old user ID to replace.
            new_user_id (int): The new user ID to set.
            token (str): A valid BotDetector API token.

        Raises:
            ValueError: If any of the arguments are invalid.

        Returns:
            A dictionary containing information about the number of reports that were updated.
        """
        endpoint = "/v1/report"
        params = {
            "old_user_id": old_user_id,
            "new_user_id": new_user_id,
            "token": token,
        }
        return await self._put(endpoint, params=params)

    async def get_report_count(
        self,
        name: str,
        row_count: int = 10000,
    ) -> dict:
        """
        Returns the number of reports that have been filed against the specified username.

        Args:
            name (str): The name of the user to search for.
            row_count (int, optional): The maximum number of rows to retrieve. Defaults to 10000.

        Raises:
            ValueError: If any of the arguments are invalid.

        Returns:
            A dictionary containing information about the number of reports that match the specified filters.
        """
        endpoint = "/v1/report/count"
        params = {"name": name, "row_count": row_count}
        return await self._get(endpoint, params=params)

    async def get_report_manual_count(self, name: str, row_count: int = 10000) -> dict:
        """
        Returns the number of manual reports for the given bot name.

        Args:
            name (str): The name of the bot to retrieve the report count for.
            row_count (int, optional): The maximum number of rows to return. Default is 10000.

        Raises:
            ValueError: If the provided name is invalid or if the API returns an error.

        Returns:
            A dictionary containing information about the number of reports that match the specified filters.
        """
        endpoint = "/v1/report/manual/count"
        params = {"name": name, "row_count": row_count}
        return await self._get(endpoint, params=params)
