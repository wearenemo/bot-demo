from dataclasses import dataclass


@dataclass
class PlayerPayout:
    amount: float
    bet_type_name: str
    player_id: int
