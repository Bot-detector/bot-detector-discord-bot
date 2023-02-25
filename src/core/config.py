from pydantic import BaseSettings, Field
import os


# class BaseConfig(BaseSettings):
#     class Config:
#         case_sensitive = True


class Config(BaseSettings):
    TOKEN: str
    COMMAND_PREFIX: str
    API_TOKEN: str
    MYSQL_URL: str
    API_URL: str
    WEBHOOK: str
    RELEASE_VERSION: str = "0.1"
    SECRETS: list = []

    def __init__(self, **data):
        data["SECRETS"] = [
            data["TOKEN"],
            data["API_TOKEN"],
            data["MYSQL_URL"],
            data["WEBHOOK"],
        ]
        super().__init__(**data)


CONFIG: Config = Config(
    TOKEN=os.environ.get("TOKEN"),
    COMMAND_PREFIX=os.environ.get("COMMAND_PREFIX"),
    API_TOKEN=os.environ.get("API_TOKEN"),
    MYSQL_URL=os.environ.get("SQL_URI"),
    API_URL=os.environ.get("API_URL"),
    WEBHOOK=os.environ.get("WEBHOOK"),
    RELEASE_VERSION="0.1",
)
