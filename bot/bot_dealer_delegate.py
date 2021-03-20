from discord import TextChannel

from discord.ext.commands import Bot
from game.dealer_delegate import DealerDelegate
from game.bet import ComeBet


class BotDealerDelegate(DealerDelegate):
    def __init__(self, bot: Bot, display_channel: TextChannel):
        self.bot = bot
        self.display_channel = display_channel

    async def collect_bets(self, table, pregame: bool = False):
        await self.display_channel.send('place your bets!')
        return [ComeBet(25.0, 12345)]

    async def notify_payouts(self, payouts, table, dice):
        await self.display_channel.send(f'payouts are {payouts}')
        return

    async def get_roll(self, dice, table, first_roll: bool):
        prev = str(dice)
        dice.roll()
        await self.display_channel.send(
            f'``` ROLLING \n\t{prev}\n\t{dice} ```'
        )
        return dice

    async def game_over(self, game_outcome, table, payouts, dice):
        await self.display_channel.send(f'GAME OVER! {game_outcome}\n```\t{dice}```')
