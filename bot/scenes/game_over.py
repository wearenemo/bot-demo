from utils import Text as T

class GameOverScene:

    async def show(
        self,
        roll_outcome,
        table,
        payouts,
        dice,
        next_shooter_id,
        channel
    ):
        s = T.bold('GAME OVER!')
        s += f'\n\n{T.inline_mono("$begin")} to play again'
        await channel.send(s)
