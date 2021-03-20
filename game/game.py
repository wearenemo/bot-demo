from game.dice import Dice


class Game:
    """
    Handles main game logic (but not betting)
    """

    def __init__(self):
        self.outcome = None

    @property
    def over(self):
        return bool(self.outcome)

    def update(self, roll: Dice):
        """
        TODO - get this logic right
        """
        if roll.values[0] == roll.values[1]:
            self.outcome = "Rolled doubles!"
