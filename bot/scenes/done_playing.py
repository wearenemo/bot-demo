import asyncio
from utils import Text as T


class DonePlayingScene:

    async def show(
        self,
        bot,
        table,
        last_shooter_id,
        channel
    ):
        sleep = 3.0 if not bot.TEST_MODE else 1.0
        s = T.bold('GAME OVER!') 
        s += '\nTable is empty. I\'m going to take a break.\n\nUse '
        s += f'{T.inline_mono("$help")} to learn what commands I understand.'
        s += f'\n\nIf you want to play again, do:\n{T.mono("$play")}'
        await channel.trigger_typing()
        await asyncio.sleep(sleep)
        await channel.send(s)
