from io import BytesIO

import discord
from discord.ext.commands import Context

from app.repositories.cataas import CataasAPI

api = CataasAPI()


async def cat(ctx: Context, tag=None):
    if tag is None:
        image_bytes = await api.get_random_cat()
    else:
        image_bytes = await api.get_cat_by_tag(tag)

    image_file = discord.File(BytesIO(image_bytes), filename="cat.png")
    await ctx.send(file=image_file)


async def saycat(ctx: Context, text: str):
    image_bytes = await api.get_cat_by_text(text)
    image_file = discord.File(BytesIO(image_bytes), filename="cat.png")
    await ctx.send(file=image_file)
