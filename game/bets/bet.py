from dataclasses import dataclass


@dataclass
class Bet:
    amount: float
    player_id: int
