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
        s = T.bold('Turns over! Next shooter\'s turn!')
        await channel.send(s)
