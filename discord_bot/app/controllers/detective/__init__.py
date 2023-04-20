from discord.ext.commands import Cog, Bot, Context
from app.controllers.detective import test
from discord.ext import commands
import random


class Extension(Cog, name="detective commands"):
    def __init__(self, client: Bot):
        self.client = client
