from game.bet import Bet
from game.dice import Dice


class DealerDelegate:
    """
    Abstract class / interface to be implemented by those who would
    work with Dealers
    """
    async def next_shooter(self) -> int:
        raise NotImplementedError()

    async def collect_bets(self, table, comeout: bool) -> [Bet]:
        raise NotImplementedError()

    async def notify_payouts(self, payouts, table, dice: Dice, roll_outcome):
        raise NotImplementedError()

    async def get_roll(self, dice: Dice, table, first_roll: bool) -> Dice:
        raise NotImplementedError()

    async def game_over(self, game_outcome, table, payouts, dice: Dice):
        raise NotImplementedError()
