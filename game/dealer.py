from game.dice import Dice
from game.game import Game
from game.exceptions import DealerException

import asyncio

SLEEP = 0.4

class Dealer:

    def __init__(self, table, delegate):
        self.table = table
        self.delegate = delegate
        self.game = None

    def get_dice(self):
        return Dice(2)

    def payout_bets(self, bets, rolled_dice, outcome=None):
        payouts = None
        return bets, payouts

    async def play_game(self):
        print("LETS PLAY CRAPS")
        await asyncio.sleep(SLEEP)
        game = Game()
        rolled = None
        bets = None
        while not game.over:
            print("\ngame is NOT over! Let's do it again!")
            if rolled:
                bets, payouts = self.payout_bets(bets, rolled)
                await self.delegate.notify_payouts(payouts, self.table, rolled)
                await asyncio.sleep(SLEEP)
            pregame = rolled is None
            await self.delegate.collect_bets(self.table, pregame=pregame)
            await asyncio.sleep(SLEEP)
            dice = self.get_dice()
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
        bets, payouts = self.payout_bets(bets, rolled, outcome=game.outcome)
        await self.delegate.game_over(
            game.outcome, self.table, payouts, rolled)
        return game.outcome
