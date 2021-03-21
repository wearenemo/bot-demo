from random import randint

from game.exceptions import DealerException


class Dice:
    sides = 6

    def __init__(self, num_dice: int):
        self._values = [None for i in range(num_dice)]
        self._rolled = False

    @property
    def num_dice(self):
        return len(self.values)

    @property
    def values(self):
        return self._values

    @property
    def total(self):
        return sum(self.values)

    def __str__(self):
        s = [str(v) if v else "?" for v in self.values]
        return "Dice<" + ", ".join(s) + ">"

    def roll(self):
        if self._rolled:
            raise DealerException('cant roll same dice twice')
        self._rolled = True
        self._values = [randint(1, 6) for i in range(self.num_dice)]
