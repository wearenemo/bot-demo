import argparse
import os

from discord import Member
from discord.ext.commands import check

from bot.craps_bot import CrapsBot


parser = argparse.ArgumentParser()
parser.add_argument('--channel')
parser.add_argument('--mode')
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


@bot.command(aliases=['leaders', 'top', 'winners', 'leaderboard'])
@check(is_craps_channel)
async def whales(ctx):
    """
    Show leaderboard
    """
    await bot.show_leaderboard(ctx.guild, ctx.channel)


# only disable TEST_MODE if run with:
#
# python main.py --mode deploy
TEST_MODE = True
if args.mode:
    print("bot run mode:", args.mode)
    if args.mode.lower().strip() == 'deploy':
        TEST_MODE = False

# ask andy for the token
if TEST_MODE:
    print("RUNNING IN TEST MODE")
    token = os.environ["TEST_CRAPS_TOKEN"]
else:
    print("RUNNING IN DEPLOY MODE")
    token = os.environ["CRAPS_TOKEN"]
bot.TEST_MODE = TEST_MODE
bot.run(token)
