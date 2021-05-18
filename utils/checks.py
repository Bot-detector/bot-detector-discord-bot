allowed_channels = (825189024074563614, 834028368147775488)
patron_channels = (
    834028368147775488,
    822589004028444712,
    834307018406756352,
    834307467793399808,
    830783778325528626,
    833479046821052436,
    834307018406756352,
    834307467793399808,
    843355044485136387
)


patron_roles = {
    833455217420927027,
    818528428851855361,
    830782790786220104,
    822589202964152370,
    837324705472053299,
    843356013973078037
}


async def check_allowed_channel(self, ctx):
    return not ctx.guild or ctx.channel.id in (allowed_channels + patron_channels)

async def check_patron(ctx):
    result = set(role.id for role in ctx.author.roles) & patron_roles

    if result:
        return result

    if ctx.invoked_with == "help":
        return

    await ctx.send("This is Patreon-only command. It must be ran in <#830783778325528626>")
