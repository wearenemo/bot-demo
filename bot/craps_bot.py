import discord
from discord import TextChannel

from discord.ext import commands
from game.craps import CrapsManager
from game.dealer_delegate import DealerDelegate

# from bot.scenes.begin_game import BeginGameScene


class CrapsBot(commands.Bot):
    """
    CrapsBot implements methods which are tightly coupled to
    the commands we add in main.py

    Most commands will probably just trigger "scenes" and
    update a bit of state in a CrapsGame (or whatever) object
    """

    def __init__(self, **kwargs):

        # this is where we declare what permissions the bot requires
        # in order to function. When someone adds the bot to their
        # server, they will be informed of these requirements.
        intents = discord.Intents.default()
        super().__init__(intents=intents, **kwargs)

        self.craps_manager = CrapsManager()

    async def on_ready(self):
        for g in self.guilds:
            print('creating table for', g)
            self.craps_manager.create_table(6, g.id, DealerDelegate())
        print("CrapsBot receiving crappy commands!")

    async def begin(self, channel: TextChannel):
        """
        Starts a a game in channel
        """
        print('craps manager tables are:')
        print(self.craps_manager._tables)
        table = self.craps_manager.table_for(channel.guild.id)
        # await BeginGameScene().show(channel, table, self)
        await channel.send("look at `stdout` for some gameplay action")
        await table.dealer.play_game()
