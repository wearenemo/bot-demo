import discord
from discord import Member, TextChannel

from discord.ext import commands
from game.craps import Craps

class CrapsBot(commands.Bot):

    def __init__(self, **kwargs):
        # I dont't know if we need this just playing around
        self.craps = Craps()

        # this is where we declare what permissions the bot requires
        # in order to function. When someone adds the bot to their
        # server, they will be informed of these requirements.
        intents = discord.Intents.default()

        # TODO - try running the bot without this intent before
        # deploy. We may not need it.
        intents.members = True

        super().__init__(intents=intents, **kwargs)

    async def on_ready(self):
        print("CrapsBot receiving crappy commands!")

    async def challenge(self,
                        initiator: Member,
                        opponent: Member,
                        channel: TextChannel):
        await channel.send(
            f'{initiator.mention} has challenged {opponent.mention} to '
            f'a game of Craps!'
        )
