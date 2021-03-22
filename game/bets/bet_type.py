from game.bets.payout_ratio import PayoutRatio, NoPayout


class BetType:
    """
    A BetType contains all the information about a class
    of bets (like "pass bets").

    When a player makes a bet, they create a PlayerBet which
    has an amount and a bet_type.
    """

    def __init__(
        self,
        name: str,
        payout: PayoutRatio,
        # by default a bet is never placeable or payable
        prepoint_placeable=False,
        postpoint_placeable=False,
        prepoint_payable=False,
        postpoint_payable=False,
        # all bets stay on the table by default after a
        # turn is over (maybe this shouldn't be set at here)
        stays_on_table=True,
    ):
        # if a bet stays on the table, then you sould be allowed to
        # make that bet at the start of a shoot
        if stays_on_table and not prepoint_placeable:
            raise ValueError("That doesn't really make sense")

        # I don't think there's any reason to make a bet after the point
        # is set if there's no way for that bet to pay
        if postpoint_placeable and not postpoint_payable:
            raise ValueError("Shouldn't make these kinds of bets")

        self.name = name
        self.payout = payout
        self.prepoint_placeable = prepoint_placeable
        self.postpoint_placeable = postpoint_placeable
        self.prepoint_payable = prepoint_payable
        self.stays_on_table = stays_on_table

    def __str__(self):
        return f"{self.name} - {self.payout_description}"

    def __repr__(self):
        return self.__str__()

    # override this for something with a weird name like
    # "Don't Pass"
    @property
    def cmd_name(self):
        return self.name.lower()

    # These methods are meant to be primary customization
    # site for subclasses
    def wins_prepoint(self, roll_outcome, dice):
        raise NotImplementedError()

    def wins_postpoint(self, roll_outcome, dice, point):
        raise NotImplementedError()

    def loses_prepoint(self, roll_outcome, dice):
        raise NotImplementedError()

    def loses_postpoint(self, roll_outcome, dice, point):
        raise NotImplementedError()

    def payout_description(self):
        return f"{self.name} - Pays {self.payout}"

    # Optionally overload this method, otherwise it calls the default
    # implemenation which defers to the logic specified on initialization
    def payout_for(self, roll_outcome, dice, point) -> PayoutRatio:
        return self._payout_for(roll_outcome, dice, point)

    # Internal method for implementing default behavior of payout_for
    def _payout_for(self, roll_outcome, dice, point) -> PayoutRatio:

        if point is None:
            if not self.prepoint_payable:
                return NoPayout()
            else:
                if self.wins_prepoint(roll_outcome, dice):
                    return self.payout
                else:
                    return NoPayout()
        else:
            if not self.postpoint_payable:
                return NoPayout()
            else:
                if self.wins_postpoint(roll_outcome, dice, point):
                    return self.payout
                else:
                    return NoPayout()
