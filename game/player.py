from game.exceptions import InsufficientFunds, InvalidAmount
from game.bets import PassBetType, DontPassBetType

from datetime import datetime as dt


class Player:

    MIN_NET_WORTH = 5

    def __init__(self, player_id: int, name: str, coins=500.0):
        self.id = player_id
        self.name = name
        self._coins = coins
        self._active_bets = []
        self._last_bet_at = None

    @property
    def time_since_last_bet(self):
        if self._last_bet_at is None:
            return None
        return (dt.utcnow() - self._last_bet_at).total_seconds()

    @property
    def net_worth(self):
        return self.coins + self.coins_on_table

    @property
    def coins_on_table(self):
        return sum([b.amount for b in self.active_bets])

    def __str__(self):
        s = f'{self.name} '
        s += f'[${self.coins:.0f}|${self.coins_on_table:.0f}]'
        return s

    @property
    def active_bets(self):
        return self._active_bets[:]

    @property
    def coins(self):
        return self._coins

    @property
    def has_pass_bet(self):
        for b in self.active_bets:
            if b.name == PassBetType.name:
                return True
        return False

    @property
    def has_no_pass_bet(self):
        for b in self.active_bets:
            if b.name == DontPassBetType.name:
                return True
        return False

    def pay(self, coins: float):
        if coins < 0.0:
            raise ValueError("Can't pay negative money")
        self._coins += coins

    def collect(self, coins: float):
        if coins <= 0.0:
            raise InvalidAmount("Dollar amounts must be positive")
        if coins > self._coins:
            raise InsufficientFunds("can't collect more than player has")
        self._coins -= coins

        return coins

    def place_bet(self, bet):
        """
        When a player places a bet, they "withdraw" coins from themself
        and put them into their "active bets".
        """
        try:
            wagered = self.collect(bet.amount)
            for other in self._active_bets:
                if bet.can_consolidate_with(other):
                    bet.consolidate_into(other)
                    return wagered
            self._active_bets.append(bet)
            self._last_bet_at = dt.utcnow()
            return wagered
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
        self._last_bet_at = None

    def clear_bet(self, bet_cmd_name):
        del_idx = None
        for i, b in enumerate(self._active_bets):
            if b.cmd_name == bet_cmd_name:
                del_idx = i
                to_delete = b
        if del_idx is not None:
            self._active_bets.pop(del_idx)
            self.pay(to_delete.amount)
            return to_delete
        return None

    def destroy_bets(self, bet_type_name):
        """
        Removes all bets of a certain type. Does NOT return coins to player.
        Use this to clear losing_bets.
        """
        found = True
        while found:
            found = False
            for i, b in enumerate(self._active_bets):
                if b.bet_type.name == bet_type_name:
                    found = True
                    del self._active_bets[i]
                    break
        # MAKE SURE YOU ALWAYS GOT SOME MONEY
        if self.net_worth < self.MIN_NET_WORTH:
            self.pay(self.MIN_NET_WORTH - self.net_worth)
