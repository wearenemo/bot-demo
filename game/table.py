import random
from datetime import datetime as dt

from game.exceptions import SeatsTaken, DoesNotExist, AlreadyExists
from game.dealer import Dealer
from game.player import Player
from game.dealer_delegate import DealerDelegate


class _Seat:
    """
    "private" class - helpful for Table
    """

    def __init__(self, index, player=None):
        self.index = index
        self._player = player

    def sit(self, player):
        if self.occupied:
            raise SeatsTaken("seat's taken")
        self._player = player

    def unsit(self):
        self._player = None

    @property
    def occupied(self):
        return bool(self.player)

    @property
    def empty(self):
        return not self.occupied

    @property
    def player(self):
        return self._player


class Table:

    INACTIVE_THRESH = 1.0 * 60  # 1 minute

    def __init__(self,
                 num_seats: int,
                 _id: int,
                 dealer_delegate: DealerDelegate):
        self._seats: [_Seat] = [_Seat(i) for i in range(num_seats)]
        self._players: {int: Player} = {}
        self._id = _id
        self.dealer = Dealer(self, dealer_delegate)
        self.button_position = 0
        self.point = None

    def advance_button(self):
        player_found = None
        original_position = self.button_position
        while not player_found:
            self.button_position = (self.button_position + 1) % self.num_seats
            if self.button_position == original_position:
                player_found = self._seats[original_position].player
                break
            player = self._seats[self.button_position].player
            if player:
                player_found = player
                break
        return player_found

    @property
    def all_players(self):
        return list(self._players.values())

    @property
    def is_playing(self):
        return self.dealer.is_playing

    @property
    def seats(self):
        return self._seats

    @property
    def bets(self):
        table_bets = []
        for s in self.seats:
            if s.empty:
                continue
            table_bets += s.player.active_bets[:]
        return table_bets

    def player_for(self, player_id):
        return self._players.get(player_id)

    def create_player(self, player_id, name):
        if player_id in self._players:
            raise AlreadyExists("player already exists")
        player = Player(player_id, name)
        self._players[player_id] = player
        return player

    def sit(self, player_id):
        if player_id not in self._players:
            raise DoesNotExist("player does not exist")
        for s in self.seats:
            if s.player and s.player.id == player_id:
                raise AlreadyExists("player already seated")
        player = self._players.get(player_id)
        seat = random.choice(self._available_seats())
        if not seat:
            raise SeatsTaken("table's full")
        seat.sit(player)

    def contains_player(self, player_id):
        for s in self.seats:
            if s.player and s.player.id == player_id:
                return True
        return False

    def clear(self):
        for s in self.seats:
            player = s.player
            if player is not None:
                s.unsit()
                player.clear_bets()

    def clear_inactive(self):
        now = dt.utcnow()
        cleared = []
        for s in self.seats:
            player = s.player
            if player is not None:
                inactive_time = player.time_since_last_bet
                if inactive_time:
                    if inactive_time > self.INACTIVE_THRESH:
                        s.unsit()
                        player.clear_bets()
                        cleared.append(player)
                        print("  cleared", player.name)
                else:
                    # kinda hacky but basically if we check and the player
                    # hasn't bet in previous game, we flag them for deletion
                    # next game by setting _last_bet_at
                    player._last_bet_at = now
        return cleared

    def unseat(self, player_id):
        if player_id not in self._players:
            raise DoesNotExist("player does not exist")
        for s in self.seats:
            if s.player and s.player.id == player_id:
                player = s.player
                s.unsit()
                # TODO - this might let you run away when
                # the odds get bad for your bet
                player.clear_bets()
                return player

    def _available_seats(self):
        return [s for s in self._seats if s.empty]

    def mark_active_bets(self):
        now = dt.utcnow()
        for s in self.seats:
            player = s.player
            if not player:
                continue
            if not player.active_bets:
                continue
            player._last_bet_at = now

    @property
    def num_seats(self):
        return len(self._seats)

    @property
    def seats_available(self):
        N = 0
        for s in self._seats:
            if s.empty:
                N += 1
        return N

    @property
    def full(self):
        return self.seats_available == 0

    @property
    def empty(self):
        return self.seats_available == self.num_seats
