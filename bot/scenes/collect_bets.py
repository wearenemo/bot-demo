import asyncio

from datetime import datetime as dt

from game.bet import Bet, ComeBet, PassBet

from utils import Emoji as E

class CollectBetsScene:

    def __init__(self):
        self.new_bets = []

    bets = set(['come', 'pass'])

    async def handle_bet(self, bet, msg):
        self.new_bets.append(bet)
        await msg.add_reaction(E.CHECKMARK)

    async def show(self, bot, table, comeout, display_channel):

        def check(m):
            tokens = m.content.lower().strip().split()
            bet_type = tokens[0]
            if bet_type not in self.bets:
                return False
            try:
                amount = tokens[1]
                float(amount)
                return True
            except Exception:
                return False
            return False

        await display_channel.send(
            'place your bets!')

        timeout = 15.0
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
                    bet = ComeBet(amount, u_id)
                elif bet_type == 'pass':
                    bet = PassBet(amount, u_id)
                else:
                    bet = Bet(amount, u_id)
                await self.handle_bet(bet, m)
            except asyncio.TimeoutError:
                await display_channel.send(
                    f'got {len(self.new_bets)} bets')
                break
        return self.new_bets
