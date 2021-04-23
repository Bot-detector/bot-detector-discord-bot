allowed_channels = [825189024074563614]
patron_channels = [834028368147775488, 822589004028444712, 834307018406756352, 834307467793399808, 830783778325528626]

patron_roles = [833455217420927027, 818528428851855361, 830782790786220104]


def check_allowed_channel(ctx):
    return check_channels(ctx, allowed_channels + patron_channels)


def check_patron(ctx):
    return check_channels(ctx, patron_channels) and (set([role.id for role in ctx.author.roles]) & set(patron_roles))


def check_channels(ctx, channels):
    return channels in allowed_channels or ctx.channel.type == 'dm'
