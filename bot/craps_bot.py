import discord
from discord import TextChannel

from discord.ext import commands
from game.craps import Craps

from bot.scenes.begin_game import BeginGameScene

class CrapsBot(commands.Bot):
    """
    CrapsBot implements methods which are tightly coupled to
    the commands we add in main.py

    Most commands will probably just trigger "scenes" and
    update a bit of state in a CrapsGame (or whatever) object
    """

    def __init__(self, **kwargs):
        # I dont't know if we need this just playing around
        self.craps = Craps()

        # this is where we declare what permissions the bot requires
        # in order to function. When someone adds the bot to their
        # server, they will be informed of these requirements.
        intents = discord.Intents.default()
        super().__init__(intents=intents, **kwargs)

    async def on_ready(self):
        print("CrapsBot receiving crappy commands!")

    async def begin(self, channel: TextChannel):
        """
        Starts a a game in channel
        """
        await BeginGameScene().show(channel, self)
