from utils import Text as T

from ascii_table import AsciiTable


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
        if s:
            s = T.mono("PAYOUTS / LOSSES" + s)
        outcome = T.bold(f"ROLLED {dice.total}: ") + outcome.value
        await channel.send(outcome + s)
