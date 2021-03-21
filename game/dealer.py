from game.dice import Dice
from game.bet import Bet
from game.game import Game, RollOutcome
from game.exceptions import DealerException
from game.dealer_delegate import DealerDelegate

import asyncio
SLEEP = 0.4


class Dealer:
    """
    Primary interface for bot to communicate intents regarding games.
    """

    def __init__(self, table, delegate: DealerDelegate):
        self.table = table
        self.delegate = delegate
        self.game = None

    ##################
    # Public methods

    async def play_game(self, shooter_id: int):
        print("LETS PLAY CRAPS")
        await asyncio.sleep(SLEEP)
        game = Game()
        bets = await self.delegate.collect_bets(self.table, True)
        print("GOT BETS", bets)
        while True:
            comeout = game.point is None
            dice = self._get_dice()
            rolled = await self.delegate.get_roll(
                dice, shooter_id, self.table, comeout)

            if rolled is not dice:
                raise DealerException("cheater")

            roll_outcome = game.update(rolled)
            bets, payouts = self._payout_bets(
                bets, rolled, roll_outcome)

            await self.delegate.notify_payouts(
                payouts, self.table, rolled, roll_outcome)

            if roll_outcome == RollOutcome.PointMiss7:
                shooter_id = await self.delegate.next_shooter(self.table)
                break

            await self.delegate.collect_bets(self.table, comeout)

        await self.delegate.game_over(
            roll_outcome, self.table, payouts, rolled, shooter_id)

    #################
    # Private methods

    def _get_dice(self):
        return Dice(2)

    def _payout_bets(self, bets: [Bet], rolled_dice: Dice, outcome=None):
        payouts = None
        return bets, payouts
