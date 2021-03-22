from game.bets import Bet, BetType, EvenPayout


class PassBetType(BetType):
    def __init__(self):
        super().__init__(
            "Pass",
            EvenPayout(),
            prepoint_placeable=True,
            prepoint_payable=True,
            postpoint_payable=True)

    def wins_prepoint(self, roll_outcome, dice):
        return dice.total in (7, 11)

    def wins_postpoint(self, roll_outcome, dice, point):
        return dice.total == point


class PassBet(Bet):
    def __init__(self, amount, player_id):
        super().__init__(PassBetType(), amount, player_id)
