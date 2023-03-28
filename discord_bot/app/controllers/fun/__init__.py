# /app/controllers/fun/__init__.py
from discord.ext.commands import Cog, Bot, Context
from app.controllers.fun import ping as p
from discord.ext import commands


class Extension(Cog, name="fun commands"):
    def __init__(self, client: Bot):
        self.client = client

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: Context):
        await p.mycommand(ctx)

    @commands.command()
    async def hello(self, ctx: Context):
        await ctx.send("Hello!")
