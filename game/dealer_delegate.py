from game.bets import Bet, BetType
from game.dice import Dice
from game.player_payout import PlayerPayout


class DealerDelegate:
    """
    Abstract class / interface to be implemented by those who would
    work with Dealers
    """
    async def next_shooter(
        self
    ) -> int:
        raise NotImplementedError()

    async def collect_bets(
        self,
        table,
        allowed: [BetType]
    ) -> [Bet]:
        raise NotImplementedError()

    async def notify_payouts(
        self,
        payouts: [PlayerPayout],
        table,
        dice: Dice,
        roll_outcome
    ):
        raise NotImplementedError()

    async def get_roll(
        self,
        dice: Dice,
        table,
        first_roll: bool
    ) -> Dice:
        raise NotImplementedError()

    async def game_over(
        self,
        game_outcome,
        table,
        payouts,
        dice: Dice,
        next_shooter_id: int
    ):
        raise NotImplementedError()

    async def done_playing(
        self,
        table,
        last_shooter_id
    ):
        raise NotImplementedError()
