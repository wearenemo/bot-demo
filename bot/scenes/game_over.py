class GameOverScene:

    async def show(
        self,
        game_outcome,
        table,
        payouts,
        dice,
        next_shooter_id,
        channel
    ):
        await channel.send(
            f'GAME OVER! {game_outcome}\n```\t{dice}```')
