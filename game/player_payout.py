from dataclasses import dataclass


@dataclass
class PlayerPayout:
    amount: float
    bet_type_name: str
    player_id: int

    def __str__(self):
        modifier = '+'
        if self.amount < 0.0:
            modifier = '-'
        return f'{modifier}{abs(self.amount):.0f} ({self.bet_type_name})'
