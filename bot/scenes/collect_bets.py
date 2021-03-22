import asyncio

from datetime import datetime as dt

from game import bets

from utils import Emoji as E
from utils import Text as T

from ascii_table import AsciiTable

class CollectBetsScene:

    allowed_bets = ['come', 'pass']
    timeout = 10.0

    def __init__(self):
        self.new_bets = []

    async def handle_bet(self, bet, msg):
        self.new_bets.append(bet)
        await msg.add_reaction(E.CHECKMARK)

    async def show(self, bot, table, comeout, display_channel):

        def check(m):
            tokens = m.content.lower().strip().split()
            bet_type = tokens[0]
            if bet_type not in self.allowed_bets:
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

        valid_bets = ", ".join([T.inline_mono(b) for b in self.allowed_bets])
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
                print('time left', left)
                if left < 0.0:
                    raise asyncio.TimeoutError()
                m = await bot.wait_for('message', check=check, timeout=left)
                tokens = m.content.lower().strip().split()
                bet_type = tokens[0]
                amount = float(tokens[1])
                u_id = m.author.id
                if bet_type == 'come':
                    bet = bets.Come(amount, u_id)
                elif bet_type == 'pass':
                    bet = bets.Pass(amount, u_id)
                else:
                    bet = bets.Bet(amount, u_id)
                await self.handle_bet(bet, m)
            except asyncio.TimeoutError:
                await bet_msg.add_reaction(E.HOURGLASS)
                break
        return self.new_bets
