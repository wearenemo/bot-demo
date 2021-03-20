import discord
from discord import TextChannel

from discord.ext import commands
from game.craps import CrapsManager
from bot.bot_dealer_delegate import BotDealerDelegate

from bot.scenes.begin_game import BeginGameScene


class CrapsBot(commands.Bot):
    """
    CrapsBot implements methods which are tightly coupled to
    the commands we add in main.py

    Most commands will probably just trigger "scenes" and
    update a bit of state in a CrapsGame (or whatever) object
    """

    CRAPS_CHANNEL_NAME = "craps"

    def __init__(self, **kwargs):

        # this is where we declare what permissions the bot requires
        # in order to function. When someone adds the bot to their
        # server, they will be informed of these requirements.
        intents = discord.Intents.default()
        super().__init__(intents=intents, **kwargs)

        self.craps_manager = CrapsManager()

    async def on_ready(self):
        for g in self.guilds:
            for c in g.channels:
                if c.name == self.CRAPS_CHANNEL_NAME:
                    print('creating table for', g)
                    delegate = BotDealerDelegate(self, c)
                    self.craps_manager.create_table(6, g.id, delegate)
        print("CrapsBot receiving crappy commands!")

    async def begin(self, channel: TextChannel):
        """
        Starts a a game in channel
        """
        print(self.craps_manager._tables)
        table = self.craps_manager.table_for(channel.guild.id)
        delegate = table.dealer.delegate
        if isinstance(delegate, BotDealerDelegate):
            if delegate.display_channel != channel:
                return await channel.send(
                    f"This isn't where we play craps! Try "
                    f"#{self.CRAPS_CHANNEL_NAME}")
        await BeginGameScene().show(channel, self)
        await table.dealer.play_game()
