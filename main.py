import argparse
import os

from discord import Member
from discord.ext.commands import check

from bot.craps_bot import CrapsBot


parser = argparse.ArgumentParser()
parser.add_argument('--channel')
args = parser.parse_args()


bot = CrapsBot(command_prefix='$')
if args.channel:
    bot.CRAPS_CHANNEL_NAME = args.channel


async def is_craps_channel(ctx):
    return ctx.channel and ctx.channel.name == bot.CRAPS_CHANNEL_NAME


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
@check(is_craps_channel)
async def play(ctx):
    """
    Begin a game of craps
    """
    await bot.begin(ctx.author, ctx.channel)


@bot.command()
@check(is_craps_channel)
async def leave(ctx):
    """
    Leave the table
    """
    await bot.leave(ctx.author, ctx.channel)


@bot.command()
@check(is_craps_channel)
async def me(ctx):
    """
    Show active bets
    """
    await bot.me(ctx.author, ctx.channel)


@bot.command()
@check(is_craps_channel)
async def tip(ctx, player: Member, amount: int):
    """
    Tip another player
    """
    await bot.tip(ctx.author, player, amount, ctx.channel)


@bot.command()
@check(is_craps_channel)
async def clear(ctx, bet: str):
    """
    Clear bet from table

    If you want to get rid of your place4 bet, do:

      $clear place4
    """
    await bot.clear_bet(ctx.author, bet, ctx.channel)


# ask andy for the token
bot.run(os.environ["CRAPS_TOKEN"])
