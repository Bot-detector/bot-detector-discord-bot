allowed_channels = [825189024074563614, 833479046821052436, 822589004028444712, 830783778325528626, 834028368147775488]


def check_allowed_channel(ctx):
    return ctx.channel.id in allowed_channels or ctx.channel.type == 'dm'
