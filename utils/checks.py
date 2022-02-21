from re import A


allowed_channels = (825189024074563614, 834028368147775488, 837779037900374059, 830545391119499294, 890723372307198003)


patron_channels = (
    834028368147775488,
    822589004028444712,
    834307018406756352,
    834307467793399808,
    830783778325528626,
    833479046821052436,
    834307018406756352,
    834307467793399808,
    843355044485136387,
    850903158754115584,
    852601541567184916,
    853384585949478972,
    854103445304115260,
    859376237902299167,
    886736407752736788,
    883148692306133052,
    830545391119499294,
    890723372307198003
)


patron_roles = {
    833455217420927027,
    818528428851855361,
    830782790786220104,
    822589202964152370,
    837324705472053299,
    843356013973078037
}


admin_roles = {
    817917060796776469,
    817917814798155866,
    818528428851855361
}


async def check_allowed_channel(self, ctx):
    if str(ctx.command) == "panic":
        return True
    elif await is_admin(ctx):
        return True
    else:
        return not ctx.guild or ctx.channel.id in (allowed_channels + patron_channels)


async def check_patron(ctx):
    result = set(role.id for role in ctx.author.roles) & patron_roles

    if result:
        return result
    elif await is_admin(ctx):
        return True
    elif ctx.invoked_with == "help":
        return


async def is_admin(ctx):
    return set(role.id for role in ctx.author.roles) & admin_roles
