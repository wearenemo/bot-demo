from game.exceptions import InsufficientFunds


class Player:
    def __init__(self, player_id: int, name: str, coins=500.0):
        self.id = player_id
        self.name = name
        self._coins = coins

    @property
    def coins(self):
        return self._coins

    def pay(self, coins: float):
        self._coins += coins

    def collect(self, coins: float):
        if coins > self._coins:
            raise InsufficientFunds("can't collect more than player has")
        self._coins -= coins
        return coins
