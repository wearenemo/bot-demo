from game.bet import ComeBet

class DealerDelegate:

    async def collect_bets(self, table, pregame=False):
        return ComeBet(25.0, 12345)

    async def notify_payouts(self, payouts, table, dice):
        return

    async def get_roll(self, dice, table, first_roll):
        dice.roll()
        return dice

    async def game_over(self, game_outcome, table, payouts, dice):
        print("\n\nGAME OVER\n", dice, "\n")
