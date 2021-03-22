from game.bets import BetType, Bet, EvenPayout


class DontPassBetType(BetType):

    name = "Don't Pass"

    def __init__(self):
        super().__init__(
            self.name,
            EvenPayout(),
            prepoint_placeable=True,
            prepoint_payable=True,
            postpoint_payable=True)

    @property
    def cmd_name(self):
        return "nopass"

    def wins_prepoint(self, roll_outcome, dice):
        return dice.total in set([2, 3])

    def wins_postpoint(self, roll_outcome, dice, point):
        return dice.total == 7

    def loses_prepoint(self, roll_outcome, dice):
        return dice.total in set([7, 11, 12])

    def loses_postpoint(self, roll_outcome, dice, point):
        return dice.total == point


class DontPassBet(Bet):
    def __init__(self, amount, player_id):
        super().__init__(DontPassBetType(), amount, player_id)
