from dataclasses import dataclass

from game.bets import BetType


@dataclass
class Bet:
    bet_type: BetType
    amount: float
    player_id: int

    @property
    def name(self):
        return self.bet_type.name

    @property
    def cmd_name(self):
        return self.bet_type.cmd_name

    def can_consolidate_with(self, other):
        return other.cmd_name == self.cmd_name

    def consolidate_into(self, other):
        if self.can_consolidate_with(other):
            other.amount += self.amount

    def __str__(self):
        potential = self.bet_type.payout.payout_for(self.amount)
        amt = f"{self.amount:.0f}"
        return f"'{self.cmd_name} {amt}' - Pays ${potential:.0f} on ${amt}"

    def __repr__(self):
        return self.__str__()
