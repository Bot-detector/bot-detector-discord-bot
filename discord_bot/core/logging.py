import logging
import sys
import json

# setup logging
stream_handler = logging.StreamHandler(sys.stdout)
# # log formatting
formatter = logging.Formatter(
    json.dumps(
        {
            "ts": "%(asctime)s",
            "name": "%(name)s",
            "function": "%(funcName)s",
            "level": "%(levelname)s",
            "msg": "%(message)s",
        }
    )
)

stream_handler.setFormatter(formatter)

handlers = [stream_handler]
logging.basicConfig(level=logging.INFO, handlers=handlers)
logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("discord.client").setLevel(logging.WARNING)
logging.getLogger("discord.gateway").setLevel(logging.WARNING)
