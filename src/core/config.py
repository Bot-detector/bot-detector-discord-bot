from pydantic import BaseSettings, Field
import os


class Config(BaseSettings):
    COMMAND_PREFIX: str
    API_TOKEN: str
    MYSQL_URL: str
    API_URL: str
    WEBHOOK: str
    BEARER: str
    RELEASE_VERSION: str = "0.1"
    SECRETS: list = []

    def __init__(self, **data):
        data["SECRETS"] = [
            data["API_TOKEN"],
            data["MYSQL_URL"],
            data["WEBHOOK"],
            data["BEARER"],
        ]
        super().__init__(**data)


CONFIG: Config = Config(
    COMMAND_PREFIX=os.environ.get("COMMAND_PREFIX"),
    API_TOKEN=os.environ.get("API_TOKEN"),
    MYSQL_URL=os.environ.get("SQL_URI"),
    API_URL=os.environ.get("API_URL"),
    WEBHOOK=os.environ.get("WEBHOOK"),
    RELEASE_VERSION="0.1",
    BEARER=os.environ.get("BEARER"),
)
