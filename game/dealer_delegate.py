from game.bet import Bet, ComeBet
from game.dice import Dice


class DealerDelegate:
    """
    Abstract class / interface to be implemented by those who would
    work with Dealers
    """
    async def collect_bets(self, table, pregame: bool = False) -> [Bet]:
        return [ComeBet(25.0, 12345)]

    async def notify_payouts(self, payouts, table, dice: Dice):
        return

    async def get_roll(self, dice: Dice, table, first_roll: bool) -> Dice:
        dice.roll()
        return dice

    async def game_over(self, game_outcome, table, payouts, dice: Dice):
        print("\n\nGAME OVER\n", dice, "\n")
