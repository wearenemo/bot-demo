import asyncio

import discord
from discord import TextChannel, Member

from discord.ext import commands
from game.craps import CrapsManager
from bot.bot_dealer_delegate import BotDealerDelegate

from bot.scenes.begin_game import BeginGameScene

from game.exceptions import AlreadyExists, SeatsTaken, CrapsException

from utils import Text as T


class CrapsBot(commands.Bot):
    """
    CrapsBot implements methods which are tightly coupled to
    the commands we add in main.py

    Most commands will probably just trigger "scenes" and
    update a bit of state in a CrapsGame (or whatever) object
    """

    CRAPS_CHANNEL_NAME = "craps"
    SEATS_PER_TABLE = 9

    def __init__(self, **kwargs):

        # this is where we declare what permissions the bot requires
        # in order to function. When someone adds the bot to their
        # server, they will be informed of these requirements.
        intents = discord.Intents.default()
        super().__init__(intents=intents, **kwargs)

        self.craps_manager = CrapsManager()

    async def allowed_channel(self, channel):
        """
        preprocessing that we probably want to do on every cmd
        """
        table = self.craps_manager.table_for(channel.guild.id)
        delegate = table.dealer.delegate
        if isinstance(delegate, BotDealerDelegate):
            if delegate.display_channel != channel:
                await channel.send(
                    f"This isn't where we play craps! Try "
                    f"#{self.CRAPS_CHANNEL_NAME}")
                raise CrapsException("we don't play craps here")
        return table, delegate

    async def on_ready(self):
        for g in self.guilds:
            for c in g.channels:
                if c.name == self.CRAPS_CHANNEL_NAME:
                    print('creating table for', g)
                    delegate = BotDealerDelegate(self, c)
                    self.craps_manager.create_table(
                        self.SEATS_PER_TABLE, g.id, delegate)
                    break
            else:
                raise Exception(
                    f'Channel {self.CRAPS_CHANNEL_NAME} does not exist')
        print("CrapsBot receiving crappy commands!")

    async def begin(self, channel: TextChannel):
        """
        Starts a a game in channel
        """
        table, delegate = await self.allowed_channel(channel)
        responses = await BeginGameScene().show(channel, self)
        playing = []
        for r in responses:
            try:
                player = table.create_player(
                    r.member.id, r.member.display_name)
                table.sit(player.id)
                playing.append(r.member)
            except AlreadyExists:
                player = table.player_for(r.member.id)
                try:
                    table.sit(player.id)
                    playing.append(r.member)
                except AlreadyExists:
                    playing.append(r.member)
            except SeatsTaken:
                await channel.send(
                    f"Sorry {r.member.mention}, the table is full.")

        shooter = table.advance_button()
        shooter_member = None
        for p in playing:
            if p.id == shooter.id:
                shooter_member = p
                break
        if not shooter_member:
            raise CrapsException("No shooter!")

        player_str = 'Playing craps with: ' + ",".join([p.name for p in playing])

        async with channel.typing():
            await asyncio.sleep(3.0)
            await channel.send(
                f'\n{T.bold(player_str)}\n'
                f"{shooter_member.mention} has the dice. Let's hope they're hot!\n"
            )
        await asyncio.sleep(1.5)
        await table.dealer.play(player.id)

    async def leave(self, member: Member, channel: TextChannel):
        table, delegate = await self.allowed_channel(channel)
        player = table.player_for(member.id)
        if not player:
            return await channel.send(f'{member.name} not seated at a table!')
        unseated = table.unseat(player.id)
        summary = T.mono('  ' + str(unseated))
        await channel.send(f'{member.name} left table\n{summary}')

    async def me(self, member: Member, channel: TextChannel):
        table, delegate = await self.allowed_channel(channel)
        player = table.player_for(member.id)
        if not player:
            return await channel.send(f'{member.name} not seated at a table!')
        s = f"{str(player)}"
        if player.active_bets:
            s += "\n  "
            for ab in player.active_bets:
                s += str(ab.cmd_name) + str(ab) + "\n  "
        else:
            s += "\n  " + "NO ACTIVE BETS"
        await channel.send(T.mono(s))

    async def tip(
        self,
        sender: Member,
        recipient: Member,
        amount: int,
        channel: TextChannel
    ):
        table, delegate = await self.allowed_channel(channel)
        send_player = table.player_for(sender.id)
        if not send_player:
            return await channel.send(
                f'{sender.display_name} not seated at a table!')
        if amount > send_player.coins:
            return await channel.send(
                f'Sorry {sender.name}, you are not rich enough to do that!')
        receive_player = table.player_for(recipient.id)
        if not receive_player:
            return await channel.send(
                f'{recipient.display_name} not seated at a table!')
        coins = send_player.collect(amount)
        receive_player.pay(coins)
        return await channel.send(
            f'{sender.display_name} gave ${amount} '
            f'to {recipient.display_name}')
