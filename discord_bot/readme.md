the desing of the discord bot is similar to the api in src.

we have three folders;
- `core`: contains the configuration & setup of the discord bot.
- `cogs`: contain the business logic & the individual commands of the discord bot.
- `repositories`: contain the different api's the system is calling for data.

```mermaid
flowchart LR
    user <--> |/command| discord_bot.core.client
    discord_bot.core.client <--> |logic & commands| discord_bot.cogs

    discord_bot.cogs.command <--> |command| discord_bot.cogs.event
    discord_bot.cogs.command <--> |command| discord_bot.cogs.fun
    discord_bot.cogs.command <--> |command| discord_bot.cogs.linking
    discord_bot.cogs.command <--> |command| discord_bot.cogs.map
    discord_bot.cogs.command <--> |command| discord_bot.cogs.mod
    discord_bot.cogs.command <--> |command| discord_bot.cogs.stats

    discord_bot.cogs <--> |data| discord_bot.repositories

    discord_bot.repositories.repo <--> |request| discord_bot.repositories.bot_detector_discord
    discord_bot.repositories.repo <--> |request| discord_bot.repositories.cataas
    discord_bot.repositories.repo <--> |request| discord_bot.repositories.shibe
    discord_bot.repositories.repo <--> |request| discord_bot.repositories.some_random_api
```
