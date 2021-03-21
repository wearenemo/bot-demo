import asyncio
from utils import Emoji as E


class GetRollScene:

    timeout = 10.0

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
        waiting = await display_channel.send(
            f'Waiting {self.timeout:.0f} seconds for {user.mention} to `roll`...'
        )

        def check(m):
            if m.content.strip().lower() != 'roll':
                return False
            if m.author.id != shooter_id:
                return False
            return True

        try:
            m = await bot.wait_for(
                'message', check=check, timeout=self.timeout)
            await m.add_reaction(E.DIE)
        except asyncio.TimeoutError:
            async with display_channel.typing():
                await waiting.add_reaction(E.HOURGLASS)
                asyncio.sleep(0.5)
                new_content = waiting.content + " nevermind, I can do it for you."
                await waiting.edit(content=new_content)
            await asyncio.sleep(1.0)
        dice.roll()
        return dice
