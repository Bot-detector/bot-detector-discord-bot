import aiohttp
import logging

logger = logging.getLogger(__name__)


class ShibeAPI:
    """
    A client for the Shibe Online API.
    """

    def __init__(self) -> None:
        self.base_url = "https://shibe.online/api"

    async def _get_urls(self, url: str) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                return data

    async def get_cats(self, count: int = 1) -> list:
        """
        Retrieve one or more random cat image URLs.

        Args:
            count (int): The number of cat image URLs to retrieve.

        Returns:
            list: A list of URLs representing the cat images.
        """
        url = f"{self.base_url}/cats?count={count}&urls=true"
        return await self._get_urls(url)

    async def get_shibes(self, count: int = 1) -> list:
        """
        Retrieve one or more random shibe image URLs.

        Args:
            count (int): The number of shibe image URLs to retrieve.

        Returns:
            list: A list of URLs representing the shibe images.
        """
        url = f"{self.base_url}/shibes?count={count}&urls=true"
        return await self._get_urls(url)

    async def get_birds(self, count: int = 1) -> list:
        """
        Retrieve one or more random bird image URLs.

        Args:
            count (int): The number of bird image URLs to retrieve.

        Returns:
            list: A list of URLs representing the bird images.
        """
        url = f"{self.base_url}/birds?count={count}&urls=true"
        return await self._get_urls(url)
