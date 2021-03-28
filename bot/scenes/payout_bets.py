import asyncio

from utils import Text as T


class PayoutBetsScene:
    async def show(
        self,
        bot,
        payouts,
        table,
        dice,
        outcome,
        channel
    ):
        by_player = {}
        payouts_exist = False
        for p in payouts:
            if p.player_id not in by_player:
                by_player[p.player_id] = []
            by_player[p.player_id].append(p)
        s = ""
        for seat in table.seats:
            if seat.empty:
                continue
            player = seat.player
            payouts = by_player.get(player.id)
            if not payouts:
                continue
            s += f'  \n\n{player}\n    '
            s += '\n    '.join([str(po) for po in payouts])
            payouts_exist = True
        if s:
            s = T.mono("PAYOUTS / LOSSES" + s)
        outcome = T.bold(f"ROLLED {dice.total}: ") + outcome.value
        await channel.send(outcome + s)
        sleep = 4.0
        if bot.TEST_MODE:
            sleep = 1.0
        if payouts_exist:
            await channel.trigger_typing()
            await asyncio.sleep(sleep)
