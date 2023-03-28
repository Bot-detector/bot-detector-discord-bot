from discord.ext.commands import Bot
from controllers import event, fun, linking, map, mod, stats


def setup(client: Bot):
    client.add_cog(event.Extension(client))
    client.add_cog(fun.Extension(client))
    client.add_cog(linking.Extension(client))
    client.add_cog(map.Extension(client))
    client.add_cog(mod.Extension(client))
    client.add_cog(stats.Extension(client))
