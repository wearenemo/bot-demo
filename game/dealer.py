from datetime import datetime as dt

from game.dice import Dice
from game.bets import Bet, PassBetType, DontPassBetType
from game.bets import Place4BetType, Place5BetType, Place6BetType
from game.bets import Place8BetType, Place9BetType, Place10BetType
from game.game import Game, RollOutcome

from game.player_payout import PlayerPayout
from game.exceptions import DealerException, CrapsException
from game.dealer_delegate import DealerDelegate


class Dealer:
    """
    Primary interface for bot to communicate intents regarding games.
    """

    allowed_bet_types = [
        PassBetType(),
        DontPassBetType(),
        Place4BetType(),
        Place5BetType(),
        Place6BetType(),
        Place8BetType(),
        Place9BetType(),
        Place10BetType()]

    def __init__(self, table, delegate: DealerDelegate):
        self.table = table
        self.delegate = delegate
        self.game = None

    @property
    def is_playing(self):
        return self.game is not None

    ##################
    # Public methods

    async def play(self, shooter_id: int):
        """
        Keep playing as long as the table has a player
        """
        now = dt.utcnow()
        for s in self.table.seats:
            if not s.empty:
                s.player._last_bet_at = now
        while not self.table.empty:
            try:
                self.game = Game()
                await self.play_game(shooter_id)
                shooter = self.table.advance_button()
                if not shooter:
                    break
                shooter_id = shooter.id
                self.table.save_players()

                self.game = None
            except Exception as exc:
                self.game = None
                self.table.clear()
                await self.delegate.report_exception(exc)
        await self.delegate.done_playing(self.table, shooter_id)

    async def play_game(self, shooter_id: int):
        """
        Play for one shooter's turn
        """
        if not self.game:
            raise CrapsException("No game to play!")

        cleared = self.table.clear_inactive()
        if cleared:
            await self.delegate.notify_cleared_players(cleared)

        await self.delegate.collect_bets(self.table, self._allowed_bet_types())

        while True:
            game = self.game
            if game is None:
                raise CrapsException("no game to play. Can't get roll")
            comeout = game.point is None
            dice = self._get_dice()
            if not self.table.contains_player(shooter_id):
                shooter = self.table.advance_button()
                if not shooter:
                    shooter_id = None
                else:
                    shooter_id = shooter.id
            rolled = await self.delegate.get_roll(
                dice, shooter_id, self.table, comeout)

            if rolled is not dice:
                raise DealerException("cheater")
            game = self.game
            if game is None:
                raise CrapsException("no game to play. Can't payout bets.")
            roll_outcome = game.update(rolled)
            payouts = self._payout_bets(
                self.table.bets, rolled, roll_outcome, self.table.point)
            self.table.point = game.point
            self.table.mark_active_bets()
            self.table.save_players()

            await self.delegate.notify_payouts(
                payouts, self.table, rolled, roll_outcome)

            if roll_outcome == RollOutcome.PointMiss7:
                shooter_id = await self.delegate.next_shooter(self.table)
                break

            await self.delegate.collect_bets(
                self.table, self._allowed_bet_types())

        await self.delegate.game_over(
            roll_outcome, self.table, payouts, rolled, shooter_id)
        self.game = None

    #################
    # Private methods

    def _allowed_bet_types(self):
        allowed = []
        prepoint = self.table.point is None
        for bt in self.allowed_bet_types:
            if prepoint:
                if bt.prepoint_placeable:
                    allowed.append(bt)
            else:
                if bt.postpoint_placeable:
                    allowed.append(bt)
        return allowed

    def _verify_and_place_bets(self, bets):
        for b in bets:
            bet_type = b.bet_type
            if self.table.point is None:
                if not bet_type.prepoint_placeable:
                    # TODO notify delegate of invalid bet
                    print("CAN'T PLACE BET! Not prepoint placeable")
                    continue
            else:
                if not bet_type.postpoint_placeable:
                    # TODO notify delegate
                    print("CAN'T PLACE BET! Not postpoint placeable")
                    continue
            p_id = b.player_id
            player = self.table.player_for(p_id)
            if not player:
                # TODO create the player! Probably will have to ask
                # delegate for player name
                print("Can't Place bet! Player does not exit")
                continue
            amount = b.amount
            if amount > player.coins:
                # TODO notify delegate
                print("CAN'T PLACE BET! Player doesnt have the money")
                continue
            if amount <= 0.0:
                print("Can't place bet! Amounts must be positive")
                continue
            player.place_bet(b)

    def _get_dice(self):
        return Dice(2)

    def _payout_bets(self, bets: [Bet], dice: Dice, roll_outcome, point):
        # TODO - delete bets which have failed
        # 1 figure out which bets pay and which lose
        type_payouts = {}
        type_losses = {}
        for bet_type in self.allowed_bet_types:
            payout = bet_type.payout
            if point is None:
                if not bet_type.wins_prepoint(roll_outcome, dice):
                    if bet_type.loses_prepoint(roll_outcome, dice):
                        type_losses[bet_type.name] = payout
                    continue
            else:
                if not bet_type.wins_postpoint(roll_outcome, dice, point):
                    if bet_type.loses_postpoint(roll_outcome, dice, point):
                        type_losses[bet_type.name] = payout
                    continue
            if payout.pays == 0:
                continue
            type_payouts[bet_type.name] = payout

        # 2 gather payouts based on paying bets
        player_payouts = []
        for bet in bets:
            win_payout = type_payouts.get(bet.bet_type.name)
            lose_payout = type_losses.get(bet.bet_type.name)
            if not win_payout and not lose_payout:
                continue

            # okay this is kinda weird. We gather losses as
            # "negative" payouts so the delegate can do something
            # with that info too.
            if win_payout:
                amount = win_payout.payout_for(bet.amount)
            else:
                amount = -bet.amount
            if win_payout or lose_payout:
                player_payout = PlayerPayout(
                    amount,
                    bet.bet_type.name,
                    bet.player_id)
                player_payouts.append(player_payout)

        # 3 resolve payouts
        for pp in player_payouts:
            player = self.table.player_for(pp.player_id)
            if not player:
                # TODO notify delegate that player can't be paid!
                print("WHERE DID THE PLAYER GO")
                continue

            # we pay the player if they win and destroy the bet
            # if they lost
            if pp.amount > 0.0:
                player.pay(pp.amount)
            else:
                player.destroy_bets(pp.bet_type_name)

        # 4 return payouts
        return player_payouts
