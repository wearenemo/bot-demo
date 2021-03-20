from game.dice import Dice
from game.bet import Bet
from game.game import Game
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

    async def play_game(self):
        print("LETS PLAY CRAPS")
        await asyncio.sleep(SLEEP)
        game = Game()
        rolled = None
        bets = None
        while not game.over:
            print("\ngame is NOT over! Let's do it again!")
            if rolled:
                bets, payouts = self._payout_bets(bets, rolled)
                await self.delegate.notify_payouts(payouts, self.table, rolled)
                await asyncio.sleep(SLEEP)
            pregame = rolled is None
            await self.delegate.collect_bets(self.table, pregame=pregame)
            await asyncio.sleep(SLEEP)
            dice = self._get_dice()
            print('new dice\n  ', dice)
            await asyncio.sleep(SLEEP)
            rolled = await self.delegate.get_roll(
                dice,
                self.table,
                pregame)
            if rolled is not dice:
                raise DealerException("cheater")
            print('updating game with roll\n  ', rolled)
            await asyncio.sleep(SLEEP)
            game.update(rolled)
        bets, payouts = self._payout_bets(bets, rolled, outcome=game.outcome)
        await self.delegate.game_over(
            game.outcome, self.table, payouts, rolled)
        return game.outcome

    #################
    # Private methods

    def _get_dice(self):
        return Dice(2)

    def _payout_bets(self, bets: [Bet], rolled_dice: Dice, outcome=None):
        payouts = None
        return bets, payouts
