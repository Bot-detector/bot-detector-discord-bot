from discord.ext.commands import Context
from app.repositories.shibe import ShibeAPI

shibe_api = ShibeAPI()


async def dog_command(ctx: Context):
    """
    Sends a random shibe image to the channel.
    """
    shibe_url = await shibe_api.get_shibes(count=1)
    await ctx.send(shibe_url[0])


async def cat_command(ctx: Context):
    """
    Sends a random cat image to the channel.
    """
    cat_url = await shibe_api.get_cats(count=1)
    await ctx.send(cat_url[0])


async def bird_command(ctx: Context):
    """
    Sends a random bird image to the channel.
    """
    bird_url = await shibe_api.get_birds(count=1)
    await ctx.send(bird_url[0])
