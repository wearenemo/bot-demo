import argparse
import os

from discord import Member

from bot.craps_bot import CrapsBot


parser = argparse.ArgumentParser()
parser.add_argument('--channel')
args = parser.parse_args()


bot = CrapsBot(command_prefix='$')
if args.channel:
    bot.CRAPS_CHANNEL_NAME = args.channel


###################
# Bot Commands
#
# Every bot command should be listed here. The docstring for each
# command is automatically used as the help text when you do
#
# $help
#
# or
#
# $help <command>


@bot.command(aliases=["throwdown", "begin"])
async def play(ctx):
    """
    Begin a game of craps.
    """
    await bot.begin(ctx.author, ctx.channel)


@bot.command()
async def leave(ctx):
    """
    Leave the table.
    """
    await bot.leave(ctx.author, ctx.channel)


@bot.command()
async def me(ctx):
    """
    Show current active bets.
    """
    await bot.me(ctx.author, ctx.channel)


@bot.command()
async def tip(ctx, player: Member, amount: int):
    """
    Tip another player.
    """
    await bot.tip(ctx.author, player, amount, ctx.channel)


@bot.command()
async def clear(ctx, bet: str):
    """
    Clear a bet from table.

    If you want to get rid of your place4 bet, do:

      $clear place4
    """
    await bot.clear_bet(ctx.author, bet, ctx.channel)


# ask andy for the token
bot.run(os.environ["CRAPS_TOKEN"])
