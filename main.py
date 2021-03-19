import os
from discord.ext import commands
from bot.craps_bot import CrapsBot


bot = CrapsBot(command_prefix='$')


@bot.command(aliases=["throwdown"])
async def begin(ctx):
    """
    Begin a game of craps.
    """
    await bot.begin(ctx.channel)

# ask andy for the token
bot.run(os.getenv("CRAPS_TOKEN"))
