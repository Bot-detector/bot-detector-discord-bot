import logging
import aiohttp
from aiohttp import ClientSession
import re

logger = logging.getLogger(__name__)


async def _get_pastebin(url: str, session: ClientSession) -> str:
    # Replace "https://pastebin.com/" with "https://pastebin.com/raw/" in the URL
    url = url.replace("https://pastebin.com/", "https://pastebin.com/raw/")

    async with session.get(url) as resp:
        # Check if response is OK
        if not resp.ok:
            return None

        # Get response data as text
        data = await resp.text()
        return data


async def _parse_pastebin(data: str) -> list[str]:
    # Split data into a list of lines using "\r\n" as the delimiter
    user_names = [line for line in data.split("\r\n")]
    # Define a regular expression pattern to match jagex naming convention
    match = r"^[a-zA-Z0-9_\- ]{1,12}$"
    # Filter the list of usernames to only include those that match the pattern
    user_names = [name for name in user_names if re.match(match, name)]
    # Remove duplicates from the list
    user_names = list(set(user_names))
    logger.debug(f"parsed names: {len(user_names)}")
    return user_names


def _batch(iterable, n=1) -> list:
    # Loop through the iterable in increments of size n and yield the next batch as a list
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]
