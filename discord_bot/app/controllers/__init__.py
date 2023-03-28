# app/controllers/__init__.py
from discord.ext.commands import Bot
from . import event, fun, linking, map, mod, stats
import logging

logger = logging.getLogger(__name__)


async def setup(bot: Bot):
    await bot.add_cog(event.Extension(bot))
    await bot.add_cog(fun.Extension(bot))
    await bot.add_cog(linking.Extension(bot))
    await bot.add_cog(map.Extension(bot))
    await bot.add_cog(mod.Extension(bot))
    await bot.add_cog(stats.Extension(bot))

    logger.info("setup success")
