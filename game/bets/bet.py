from dataclasses import dataclass


@dataclass
class Bet:
    amount: float
    player_id: int

class PassBet(Bet): pass;
class DontPassBet(Bet): pass;
class ComeBet(Bet): pass;
