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
        await channel.send(T.bold(outcome.value))
