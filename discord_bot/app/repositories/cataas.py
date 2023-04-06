import aiohttp
import logging

logger = logging.getLogger(__name__)


class CataasAPI:
    """
    A client for the Cat as a Service (CATAAS) API.
    """

    def __init__(self) -> None:
        self.base_url = "https://cataas.com/cat"

    async def _make_request(self, url: str) -> bytes:
        """
        Helper method to make a web request and return the response content as bytes.

        Args:
        url (str): The URL to request.

        Returns:
        bytes: The response content as bytes.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_content = await response.read()
                logger.info(f"Received response from {url}")
                return response_content

    async def get_random_cat(self) -> bytes:
        """
        Retrieve a random cat image.

        Returns:
        bytes: The bytes of the cat image.
        """
        url = self.base_url
        return await self._make_request(url)

    async def get_cat_by_tag(self, tag: str) -> bytes:
        """
        Retrieve a cat image with the specified tag.

        Args:
        tag (str): The tag to filter the cat image by.

        Returns:
        bytes: The bytes of the cat image.
        """
        url = f"{self.base_url}/{tag}"
        return await self._make_request(url)

    async def get_cat_by_text(self, text: str) -> bytes:
        """
        Retrieve a cat image with the specified text overlay.

        Args:
        text (str): The text to overlay on the cat image.

        Returns:
        bytes: The bytes of the cat image.
        """
        url = f"{self.base_url}/says/{text}"
        return await self._make_request(url)
