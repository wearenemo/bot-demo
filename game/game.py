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
        if roll.values[0] == 1:
            if roll.values[1] == 1:
                print("SNAKE EYES")
                self.outcome = "SNAKE EYES"
