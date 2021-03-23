import asyncio
from utils import Text as T
from utils import Emoji as E

class GameOverScene:

    async def show(
        self,
        bot,
        roll_outcome,
        table,
        payouts,
        dice,
        next_shooter_id,
        channel
    ):
        sleep = 0.5 if not bot.TEST_MODE else 0.1
        s = T.bold('Turns over! Next shooter\'s turn!')
        m = await channel.send(s)
        await m.add_reaction(E.SEVEN)
        await asyncio.sleep(sleep)
        await m.add_reaction(E.MONEY_WINGS)
        await asyncio.sleep(sleep)
        await m.add_reaction(E.SAD)
        await channel.trigger_typing()
        await asyncio.sleep(8 * sleep)
