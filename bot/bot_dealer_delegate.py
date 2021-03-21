from discord import TextChannel

from discord.ext.commands import Bot
from game.dealer_delegate import DealerDelegate

from bot.scenes.get_roll import GetRollScene
from bot.scenes.collect_bets import CollectBetsScene
from bot.scenes.payout_bets import PayoutBetsScene
from bot.scenes.game_over import GameOverScene


class BotDealerDelegate(DealerDelegate):
    def __init__(self, bot: Bot, display_channel: TextChannel):
        self.bot = bot
        self.display_channel = display_channel

    async def next_shooter(self, table) -> int:
        next_player = table.advance_button()
        if not next_player:
            return None
        return next_player.id

    async def collect_bets(self, table, comeout):
        return await CollectBetsScene().show(
            self.bot, table, comeout, self.display_channel)

    async def notify_payouts(self, payouts, table, dice, roll_outcome):
        return await PayoutBetsScene().show(
            self.bot, payouts, table, dice, roll_outcome, self.display_channel)

    async def get_roll(self, dice, shooter_id, table, first_roll: bool):
        return await GetRollScene().show(
            self.bot,
            dice,
            shooter_id,
            table,
            first_roll,
            self.display_channel)

    async def game_over(self,
                        game_outcome,
                        table,
                        payouts,
                        dice,
                        next_shooter_id):
        return await GameOverScene.show(
            self.bot,
            game_outcome,
            table,
            payouts,
            dice,
            next_shooter_id,
            self.display_channel)
