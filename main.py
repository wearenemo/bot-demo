import os
from discord.ext import commands
from bot.craps_bot import CrapsBot


bot = CrapsBot(command_prefix='$')


@bot.command()
async def challenge(ctx, against: commands.MemberConverter):
    """
    Challenge member to a game of craps
    """
    print('got challenge command')
    await bot.challenge(ctx.author, against, ctx.channel)

# ask andy for the token
bot.run(os.getenv("CRAPS_TOKEN"))
