class Bet:
    def __init__(self, amount, player_id: int):
        self.amount = amount
        self.player_id = player_id


class ComeBet(Bet):
    """
    an example of a concrete subclass (not fully implemented of course)
    """
    pass
