import asyncio

from discord import TextChannel

from discord.ext.commands import Bot
from game.dealer_delegate import DealerDelegate

from bot.scenes.get_roll import GetRollScene
from bot.scenes.collect_bets import CollectBetsScene
from bot.scenes.payout_bets import PayoutBetsScene
from bot.scenes.game_over import GameOverScene
from bot.scenes.done_playing import DonePlayingScene

from game.exceptions import CrapsException
from utils import Text as T


class BotDealerDelegate(DealerDelegate):
    def __init__(
        self,
        bot: Bot,
        display_channel: TextChannel
    ):

        self.bot = bot
        self.display_channel = display_channel

    async def next_shooter(
        self,
        table
    ) -> int:

        next_player = table.advance_button()
        if not next_player:
            return None
        return next_player.id

    async def collect_bets(
        self,
        table,
        allowed
    ):

        return await CollectBetsScene().show(
            self.bot,
            table,
            allowed,
            self.display_channel,
            table.dealer)

    async def notify_payouts(
        self,
        payouts,
        table,
        dice,
        roll_outcome
    ):

        await PayoutBetsScene().show(
            self.bot,
            payouts,
            table,
            dice,
            roll_outcome,
            self.display_channel)

    async def get_roll(
        self,
        dice,
        shooter_id,
        table,
        first_roll: bool
    ):
        return await GetRollScene().show(
            self.bot,
            dice,
            shooter_id,
            table,
            first_roll,
            self.display_channel)

    async def game_over(
        self,
        roll_outcome,
        table,
        payouts,
        dice,
        next_shooter_id
    ):

        return await GameOverScene().show(
            self.bot,
            roll_outcome,
            table,
            payouts,
            dice,
            next_shooter_id,
            self.display_channel)

    async def done_playing(
        self,
        table,
        last_shooter_id
    ):

        return await DonePlayingScene().show(
            self.bot,
            table,
            last_shooter_id,
            self.display_channel)

    async def report_exception(
        self,
        exception: Exception
    ):
        exception_str = T.block_quote(
            f'{T.inline_mono(type(exception))}\n{str(exception)}')
        await self.display_channel.send(
            f'Sorry to show you this, but could you let Andy know he has an '
            f'unhandled exception:\n{exception_str}',
        )
