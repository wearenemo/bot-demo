import asyncio
from utils import Emoji as E


class GetRollScene:
    async def show(
        self,
        bot,
        dice,
        shooter_id,
        table,
        first_roll,
        display_channel
    ):
        user = await bot.fetch_user(shooter_id)
        await display_channel.send(
            f'Waiting on `roll` command from {user.display_name}'
        )

        def check(m):
            if m.content.strip().lower() != 'roll':
                return False
            if m.author.id != shooter_id:
                return False
            return True

        try:
            m = await bot.wait_for(
                'message', check=check, timeout=10.0)
            await m.add_reaction(E.DIE)
        except asyncio.TimeoutError:
            await display_channel.send(
                'You are taking too long to roll. '
                'Let me roll for you.'
            )
        dice.roll()
        await display_channel.send(
            f'``` ROLLED\n\t{dice} ```'
        )
        return dice
