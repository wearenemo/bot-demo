from game.exceptions import InsufficientFunds


class Player:
    def __init__(self, player_id: int, name: str, coins=500.0):
        self.id = player_id
        self.name = name
        self._coins = coins
        self._active_bets = []

    @property
    def coins_on_table(self):
        return sum([b.amount for b in self.active_bets])

    @property
    def active_bets(self):
        return self._active_bets

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

    def place_bet(self, bet):
        """
        When a player places a bet, they "withdraw" coins from themself
        and put them into their "active bets".
        """
        print(f'place bet called on {self.name} for bet {bet}')
        try:
            self.collect(bet.amount)
            self._active_bets.append(bet)
            print(f'now i have {self.coins} coins')
        except InsufficientFunds:
            print('error!')
            raise InsufficientFunds("Can't bet more than player has")

    def clear_bets(self):
        """
        Clears active bets and returns coins to player
        """
        for b in self._active_bets:
            self.pay(b.amount)
        self._active_bets.clear()

    def destroy_bets(self, bet_type_name):
        """
        Removes all bets of a certain type. Does NOT return coins to player.
        Use this to clear losing_bets.
        """
        found = True
        print('trying to destroy bets with name', bet_type_name)
        while found:
            found = False
            for i, b in enumerate(self._active_bets):
                if b.bet_type.name == bet_type_name:
                    found = True
                    print('found bet!')
                    del self._active_bets[i]
                    break
        print('my active bets are now:', self.active_bets)
