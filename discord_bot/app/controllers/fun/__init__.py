# /app/controllers/fun/__init__.py
from discord.ext.commands import Cog, Bot, Context
from app.controllers.fun import ping as Ping, cat as Cat
from discord.ext import commands


class Extension(Cog, name="fun commands"):
    def __init__(self, client: Bot):
        self.client = client

    @commands.command()
    async def hello(self, ctx: Context):
        await ctx.send("Hello!")

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: Context):
        await Ping.ping(ctx)

    @commands.hybrid_command(name="cat")
    async def cat(self, ctx: Context, *, tag: str = None):
        await Cat.cat(ctx, tag=tag)

    @commands.hybrid_command(name="saycat")
    async def saycat(self, ctx, *, text: str):
        await Cat.saycat(ctx, text)

    @saycat.error
    @cat.error
    async def cat_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Sorry, I couldn't retrieve a cat image")
