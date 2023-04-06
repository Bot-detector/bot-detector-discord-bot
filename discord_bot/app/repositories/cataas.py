import aiohttp


class CataasAPI:
    """
    A client for the Cat as a Service (CATAAS) API.
    """

    def __init__(self) -> None:
        self.base_url = "https://cataas.com/cat"

    async def get_random_cat(self) -> bytes:
        """
        Retrieve a random cat image.

        Returns:
        bytes: The bytes of the cat image.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url) as response:
                return await response.read()

    async def get_cat_by_tag(self, tag: str) -> bytes:
        """
        Retrieve a cat image with the specified tag.

        Args:
        tag (str): The tag to filter the cat image by.

        Returns:
        bytes: The bytes of the cat image.
        """
        url = f"{self.base_url}/tag/{tag}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

    async def get_cat_by_text(self, text: str) -> bytes:
        """
        Retrieve a cat image with the specified text overlay.

        Args:
        text (str): The text to overlay on the cat image.

        Returns:
        bytes: The bytes of the cat image.
        """
        url = f"{self.base_url}/says/{text}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()
