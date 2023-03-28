from pydantic import BaseSettings
import os
import dotenv


dotenv.load_dotenv()


class Config(BaseSettings):
    BEARER: str
    COMMAND_PREFIX: str
    TOKEN: str
    RELEASE_VERSION: str = "0.1"


class Roles(BaseSettings):
    OWNER_ROLE: int
    STAFF_ROLE: int
    HEAD_DETECTIVE_ROLE: int
    DETECTIVE_ROLE: int
    PATREON_ROLE: int
    VERIFIED_PLAYER_ROLE: int
    PREVILEGED_ROLES: list = []

    def __init__(self, **data):
        print(data)
        data["PREVILEGED_ROLES"] = [data["OWNER_ROLE"], data["STAFF_ROLE"]]
        super().__init__(**data)


# id's of the commands channels
class Channels(BaseSettings):
    DETECTIVE_COMMANDS_CHANNEL: int
    DETECTIVE_LIST_SUBMISSION_CHANNEL: int
    CREATOR_COMMANDS_CHANNEL: int
    PATREON_COMMANDS_CHANNEL: int
    GENERAL_COMMANDS_CHANNEL: int
    ALLOWED_CHANNELS: list = []

    def __init__(self, **data):
        data["ALLOWED_CHANNELS"] = [
            data["DETECTIVE_COMMANDS_CHANNEL"],
            data["DETECTIVE_LIST_SUBMISSION_CHANNEL"],
            data["CREATOR_COMMANDS_CHANNEL"],
            data["PATREON_COMMANDS_CHANNEL"],
            data["GENERAL_COMMANDS_CHANNEL"],
        ]
        super().__init__(**data)


CONFIG: Config = Config(
    RELEASE_VERSION="0.1",
    TOKEN=os.environ.get("TOKEN"),
    BEARER=os.environ.get("BEARER"),
    COMMAND_PREFIX=os.environ.get("COMMAND_PREFIX"),
)

ROLES = Roles(
    OWNER_ROLE=817917060796776469,
    STAFF_ROLE=858763870042456084,
    HEAD_DETECTIVE_ROLE=855341635079503872,
    DETECTIVE_ROLE=830507560783183888,
    PATREON_ROLE=830782790786220104,
    VERIFIED_PLAYER_ROLE=831196988976529438,
)
CHANNELS = Channels(
    DETECTIVE_COMMANDS_CHANNEL=890723372307198003,
    DETECTIVE_LIST_SUBMISSION_CHANNEL=837779037900374059,
    CREATOR_COMMANDS_CHANNEL=822589004028444712,
    PATREON_COMMANDS_CHANNEL=830783778325528626,
    GENERAL_COMMANDS_CHANNEL=825189024074563614,
)
