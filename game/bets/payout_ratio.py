from dataclasses import dataclass


@dataclass
class PayoutRatio:
    pays: int  # numerator
    on: int    # denominator (cant be 0)

    def __str__(self):
        return f"${self.pays} on ${self.on}"

    def payout_for(self, amount):
        return amount * self.pays / self.on


class NoPayout(PayoutRatio):
    def __init__(self):
        self.pays = 0
        self.on = 1


class EvenPayout(PayoutRatio):
    def __init__(self):
        self.pays = 1
        self.on = 1
