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
    OWNER_ROLE: int = 817917060796776469
    STAFF_ROLE: int = 858763870042456084
    HEAD_DETECTIVE_ROLE: int = 855341635079503872
    DETECTIVE_ROLE: int = 830507560783183888
    PATREON_ROLE: int = 830782790786220104
    VERIFIED_PLAYER_ROLE: int = 831196988976529438
    PREVILEGED_ROLES: list = []

    def __init__(self, **data):
        data["PREVILEGED_ROLES"] = [
            data["OWNER_ROLE"],
            data["STAFF_ROLE"],
        ]


# id's of the commands channels
class Channels(BaseSettings):
    DETECTIVE_COMMANDS_CHANNEL: int = 890723372307198003
    DETECTIVE_LIST_SUBMISSION_CHANNEL: int = 837779037900374059
    CREATOR_COMMANDS_CHANNEL: int = 822589004028444712
    PATREON_COMMANDS_CHANNEL: int = 830783778325528626
    GENERAL_COMMANDS_CHANNEL: int = 825189024074563614
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

ROLES = Roles()
CHANNELS = Channels()
