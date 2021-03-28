from enum import Enum

from game.dice import Dice


class RollOutcome(Enum):
    Natural = "Natural. Pass bets win!"
    Craps   = "Craps. Pass bets lose."
    PointSet = "Point set. Shooter keeps dice."
    PointHit = "Shooter hit the point! Shooter keeps dice."
    PointMiss7 = "Shooter missed point with 7. Shooter loses dice."
    PointContinues = "Point missed. Shooter keeps dice."


class Game():
    """
    Handles main game logic for one shooter's turn
    https://en.wikipedia.org/wiki/Craps#Rules_of_play
    """

    def __init__(self):
        self.point = None

    def update(self, roll: Dice):
        total = roll.total
        # no point set yet
        if self.point is None:
            if total in (7, 11):
                return RollOutcome.Natural

            elif total in (2, 3, 12):
                return RollOutcome.Craps

            else:
                self.point = total
                return RollOutcome.PointSet

        else:
            if total == self.point:
                self.point = None
                return RollOutcome.PointHit
            elif total == 7:
                self.point = None
                return RollOutcome.PointMiss7
            else:
                return RollOutcome.PointContinues
