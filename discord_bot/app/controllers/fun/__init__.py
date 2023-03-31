# /app/controllers/fun/__init__.py
from discord.ext.commands import Cog, Bot, Context
from app.controllers.fun import ping as Ping
from discord.ext import commands


class Extension(Cog, name="fun commands"):
    def __init__(self, client: Bot):
        self.client = client

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: Context):
        await Ping.ping(ctx)

    @commands.command()
    async def hello(self, ctx: Context):
        await ctx.send("Hello!")
