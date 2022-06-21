import json
import logging
import os
import sys

import dotenv

dotenv.load_dotenv(dotenv.find_dotenv(), verbose=True)

TOKEN = os.environ.get('TOKEN')
COMMAND_PREFIX = os.environ.get('COMMAND_PREFIX')


# setup logging
file_handler = logging.FileHandler(filename="./error.log", mode='a')
stream_handler = logging.StreamHandler(sys.stdout)
# # log formatting
formatter = logging.Formatter(json.dumps(
    {
        'ts': '%(asctime)s',
        'name': '%(name)s',
        'function': '%(funcName)s',
        'level':'%(levelname)s',
        'msg': '%(message)s'
    }
))


file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

handlers = [
    file_handler,
    stream_handler
]

logging.basicConfig(level=logging.DEBUG, handlers=handlers)

logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.DEBUG)