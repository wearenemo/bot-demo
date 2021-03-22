import argparse
import os

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


@bot.command(aliases=["throwdown"])
async def begin(ctx):
    """
    Begin a game of craps.
    """
    await bot.begin(ctx.channel)

# ask andy for the token
bot.run(os.environ["CRAPS_TOKEN"])
