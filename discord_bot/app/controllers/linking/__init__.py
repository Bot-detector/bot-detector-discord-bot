from discord.ext.commands import Cog, Bot


class Extension(Cog, name="linking commands"):
    def __init__(self, client: Bot):
        self.client = client
