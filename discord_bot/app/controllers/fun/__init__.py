from discord.ext.commands import Cog, Bot


class Extension(Cog, name="fun commands"):
    def __init__(self, client: Bot):
        self.client = client