from pydantic import BaseSettings, Field
import os


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True


class Config(BaseConfig):
    TOKEN: str = Field(default_factory=os.environ.get("TOKEN"))
    COMMAND_PREFIX: str = Field(default_factory=os.environ.get("COMMAND_PREFIX"))
    API_TOKEN: str = Field(default_factory=os.environ.get("API_TOKEN"))
    MYSQL_URL: str = Field(default_factory=os.environ.get("SQL_URI"))
    API_URL: str = Field(default_factory=os.environ.get("API_URL"))
    WEBHOOK: str = Field(default_factory=os.environ.get("WEBHOOK"))
    RELEASE_VERSION: str = "0.1"
    SECRETS: list = [TOKEN, API_TOKEN, API_URL, WEBHOOK]


CONFIG: Config = Config()
