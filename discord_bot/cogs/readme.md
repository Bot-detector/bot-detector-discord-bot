because the methods of cogs can get big, we define the cog in the __init__.py file of the folder and have a file for each method.

we can create the cog as following
```py
# discord_bot/cogs/stats/__init__.py
class PlayerStatsCommands(Cog):
    def __init__(self, bot: discord.Client) -> None:
        """
        Initialize the playerStatsCommands class.
        :param bot: The discord bot client.
        """
        self.bot = bot

    from .lookup import lookup

# discord_bot/cogs/stats/lookup.py
@commands.hybrid_command()
@commands.has_any_role(VERIFIED_PLAYER_ROLE)  # verified
async def lookup(self, ctx: Context, *, player_name):
  # do something
  pass
```
