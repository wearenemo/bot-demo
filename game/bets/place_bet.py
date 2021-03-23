from game.bets import Bet, BetType, PayoutRatio


class PlaceBetType(BetType):

    name = "Place"
    cmd_name = "place"

    def __init__(self, N):
        if N in (6, 8):
            payout = PayoutRatio(7, 6)
        elif N in (5, 9):
            payout = PayoutRatio(7, 5)
        elif N in (4, 10):
            payout = PayoutRatio(9, 5)
        else:
            raise ValueError("invalid target for place bet")
        super().__init__(
            self.__class__.name + ' ' + str(N),
            payout,
            postpoint_placeable=True,
            postpoint_payable=True,
            stays_on_table=False)
        self.N = N
        self.cmd_name = "place" + str(N)

    def wins_prepoint(self, roll_outcome, dice):
        return False

    def loses_prepoint(self, roll_outcome, dice):
        return False

    def wins_postpoint(self, roll_outcome, dice, point):
        return dice.total == self.N

    def loses_postpoint(self, roll_outcome, dice, point):
        return dice.total == 7


class Place4BetType(PlaceBetType):
    def __init__(self):
        super().__init__(4)


class Place5BetType(PlaceBetType):
    def __init__(self):
        super().__init__(5)


class Place6BetType(PlaceBetType):
    def __init__(self):
        super().__init__(6)


class Place8BetType(PlaceBetType):
    def __init__(self):
        super().__init__(8)


class Place9BetType(PlaceBetType):
    def __init__(self):
        super().__init__(9)


class Place10BetType(PlaceBetType):
    def __init__(self):
        super().__init__(10)


class PlaceBet(Bet):
    def __init__(self, N, amount, player_id):
        if N == 4:
            super().__init__(Place4BetType(), amount, player_id)
        elif N == 5:
            super().__init__(Place5BetType(), amount, player_id)
        elif N == 6:
            super().__init__(Place6BetType(), amount, player_id)
        elif N == 8:
            super().__init__(Place8BetType(), amount, player_id)
        elif N == 9:
            super().__init__(Place9BetType(), amount, player_id)
        elif N == 10:
            super().__init__(Place10BetType(), amount, player_id)
        else:
            raise ValueError("Invalid N")


class Place4Bet(PlaceBet):
    def __init__(self, amount, player_id):
        super().__init__(4, amount, player_id)


class Place5Bet(PlaceBet):
    def __init__(self, amount, player_id):
        super().__init__(5, amount, player_id)


class Place6Bet(PlaceBet):
    def __init__(self, amount, player_id):
        super().__init__(6, amount, player_id)


class Place8Bet(PlaceBet):
    def __init__(self, amount, player_id):
        super().__init__(8, amount, player_id)


class Place9Bet(PlaceBet):
    def __init__(self, amount, player_id):
        super().__init__(9, amount, player_id)


class Place10Bet(PlaceBet):
    def __init__(self, amount, player_id):
        super().__init__(10, amount, player_id)


PlaceBetType.bet_class = PlaceBet

Place4BetType.bet_class = Place4Bet
Place5BetType.bet_class = Place5Bet
Place6BetType.bet_class = Place6Bet
Place8BetType.bet_class = Place8Bet
Place9BetType.bet_class = Place9Bet
Place10BetType.bet_class = Place10Bet
