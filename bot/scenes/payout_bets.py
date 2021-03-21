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
        s = AsciiTable.show_dice(dice) + T.bold(outcome.value)
        await channel.send(s)
