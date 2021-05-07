allowed_channels = [825189024074563614, 834028368147775488]
patron_channels = [834028368147775488, 822589004028444712, 834307018406756352, 834307467793399808, 830783778325528626, 833479046821052436, 834307018406756352, 834307467793399808]

patron_roles = [833455217420927027, 818528428851855361, 830782790786220104, 822589202964152370, 837324705472053299]


def check_allowed_channel(ctx):
    return check_channels(ctx, allowed_channels + patron_channels)


async def check_patron(ctx):
    result = check_channels(ctx, patron_channels) and (set([role.id for role in ctx.author.roles]) & set(patron_roles))

    if result:
        return result
    else:
        await ctx.channel.send("This is Patreon-only command. It must be ran in <#830783778325528626>")


def check_channels(ctx, channels):
    return ctx.channel.id in channels or ctx.channel.type == "dm"


