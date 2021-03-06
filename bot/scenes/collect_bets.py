import asyncio

from datetime import datetime as dt

from game import bets
from game.exceptions import AlreadyExists

from utils import Emoji as E
from utils import Text as T

from ascii_table import AsciiTable
import random

class CollectBetsScene:

    wait_messages = [
        'Wait til betting is over!',
        'Patience. We are betting.',
        'Slow your... roll! (lol seriously wait til betting is over).',
        "Can't take MDMA while collecting bets. Be patient.",
        "Laissez les bons temps attendez! (wait til we're done betting)",
        "Not so fast champ. Still betting.",
        "Go play slots if you're in such rush. We are still betting.",
        "Patience young Skywalker. A Jedi seeks not to `roll` while we are betting.",
        "Can't roll. Still betting. Maybe grab a drink?",
    ]

    def __init__(self):
        self.new_bets = []
        self.timeout = 12.0
        self.time_increase_per_bet = 10.0

    async def handle_bet(
        self, bet, msg, player, dealer, bet_msg, table, allowed_bets, remaining):
        if bet.amount > player.coins or bet.amount < 1.0:
            await msg.add_reaction(E.RED_X)
        else:
            self.new_bets.append(bet)
            dealer._verify_and_place_bets([bet])
            await bet_msg.edit(
                content=self.make_table(table, allowed_bets, remaining))
            await msg.add_reaction(E.MONEY_BAG)
            await msg.add_reaction(E.REFRESH)
            await msg.add_reaction(E.CLOCK)

    def make_table(self, table, allowed_bets, time_remaining):
        ascii_table = AsciiTable.from_table(table)

        place_bets = T.bold("Place your bets!")
        place_bets += f" You have {time_remaining:.0f} "
        if time_remaining < self.timeout:
            place_bets += "more seconds to bet..."
        else:
            place_bets += "seconds."

        valid_bets = ", ".join([T.inline_mono(b) for b in allowed_bets])
        valid_bets = T.block_quote("Valid bets are: " + valid_bets)
        return (f'{ascii_table}\n'
                f'{place_bets}\n'
                f'{valid_bets}\n')

    async def show(self, bot, table, allowed_bet_types, display_channel, dealer):

        if bot.TEST_MODE:
            self.timeout = 2.5
        else:
            if table.empty:
                self.timeout = 5.0

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
            if bet_type == 'roll':
                if m.channel == display_channel:
                    msg = random.choice(self.wait_messages)
                    asyncio.get_event_loop().create_task(
                        m.reply(msg))
            if bet_type not in allowed_bets:
                return False
            try:
                amount = tokens[1]
                float(amount)
                return True
            except Exception:
                return False
            return False

        bet_msg = await display_channel.send(
            self.make_table(table, allowed_bets, self.timeout))

        timeout = self.timeout
        start = dt.utcnow()
        while True:
            try:
                left = timeout - (dt.utcnow() - start).total_seconds()
                left = max(left, self.time_increase_per_bet)
                left = min(left, self.timeout)
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
                    player = table.create_player(u_id, m.author.display_name)
                try:
                    table.sit(player.id)
                except AlreadyExists:
                    pass
                left = timeout - (dt.utcnow() - start).total_seconds()
                left = max(left, self.time_increase_per_bet)
                left = min(left, self.timeout)
                await self.handle_bet(
                    bet, m, player, dealer, bet_msg, table, allowed_bets, left)
            except asyncio.TimeoutError:
                await bet_msg.add_reaction(E.HOURGLASS)
                break
        return self.new_bets
