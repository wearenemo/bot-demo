import asyncio

from datetime import datetime as dt

from game import bets
from game.exceptions import AlreadyExists

from utils import Emoji as E
from utils import Text as T

from ascii_table import AsciiTable

class CollectBetsScene:

    timeout = 10.0

    def __init__(self):
        self.new_bets = []

    async def handle_bet(self, bet, msg):
        self.new_bets.append(bet)
        await msg.add_reaction(E.CHECKMARK)

    async def show(self, bot, table, allowed_bet_types, display_channel):

        allowed_bets = [bt.cmd_name for bt in allowed_bet_types]

        if not allowed_bets:
            no_bets = T.block_quote("No allowed bets right now!")
            ascii_table = AsciiTable.from_table(table)
            await display_channel.send(
                f'{ascii_table}\n'
                f'{no_bets}\n')
            return []

        def check(m):
            tokens = m.content.lower().strip().split()
            bet_type = tokens[0]
            if bet_type not in allowed_bets:
                return False
            try:
                amount = tokens[1]
                float(amount)
                return True
            except Exception:
                return False
            return False

        ascii_table = AsciiTable.from_table(table)

        place_bets = T.bold("Place your bets!")
        place_bets += f" You have {self.timeout:.0f} seconds."

        valid_bets = ", ".join([T.inline_mono(b) for b in allowed_bets])
        valid_bets = T.block_quote("Valid bets are: " + valid_bets)

        bet_msg = await display_channel.send(
            f'{ascii_table}\n'
            f'{place_bets}\n'
            f'{valid_bets}\n'
        )

        timeout = self.timeout
        start = dt.utcnow()
        while True:
            try:
                left = timeout - (dt.utcnow() - start).total_seconds()
                if left < 0.0:
                    raise asyncio.TimeoutError()
                m = await bot.wait_for('message', check=check, timeout=left)
                tokens = m.content.lower().strip().split()
                bet_type = tokens[0]
                amount = float(tokens[1])
                u_id = m.author.id

                bet = None
                for bt in allowed_bet_types:
                    if bt.cmd_name == bet_type:
                        bet = bt.bet_class(amount, u_id)
                        break
                if not bet:
                    raise ValueError("No bet class found")
                player = table.player_for(u_id)
                if not player:
                    player = table.create_player(u_id)
                try:
                    table.sit(player.id)
                except AlreadyExists:
                    pass
                await self.handle_bet(bet, m)
            except asyncio.TimeoutError:
                await bet_msg.add_reaction(E.HOURGLASS)
                break
        return self.new_bets
