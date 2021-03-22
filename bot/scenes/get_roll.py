import asyncio
from utils import Emoji as E
from datetime import datetime as dt
from game.dice import Dice
from ascii_table import AsciiTable


class GetRollScene:

    timeout = 10.0

    roll_duration = 2.0

    async def show(
        self,
        bot,
        dice,
        shooter_id,
        table,
        first_roll,
        display_channel
    ):
        if shooter_id:
            user = await bot.fetch_user(shooter_id)
            waiting = await display_channel.send(
                f'Waiting {self.timeout:.0f} seconds for {user.mention} to `roll`...'
            )
        else:
            await display_channel.send(
                f'No shooter. Auto-rolling...'
            )
            return await self.roll(dice, display_channel)

        def check(m):
            if m.content.strip().lower() != 'roll':
                return False
            if m.author.id != shooter_id:
                return False
            return True

        try:
            await bot.wait_for(
                'message', check=check, timeout=self.timeout)
        except asyncio.TimeoutError:
            async with display_channel.typing():
                await waiting.add_reaction(E.HOURGLASS)
                await asyncio.sleep(0.3)
                new_content = waiting.content + " nevermind, I can do it for you."
                await waiting.edit(content=new_content)
            await asyncio.sleep(1.0)
        finally:
            return await self.roll(dice, display_channel)

    async def roll(self, dice, display_channel):
        start = dt.utcnow()
        now = start
        new_dice = Dice(2)
        new_dice.roll()
        roll_m = await display_channel.send(AsciiTable.show_dice(new_dice))
        while (now - start).total_seconds() < self.roll_duration:
            new_dice = Dice(2)
            new_dice.roll()
            await roll_m.edit(content=AsciiTable.show_dice(new_dice))
            await asyncio.sleep(0.1)
            now = dt.utcnow()
        dice.roll()
        await roll_m.edit(content=AsciiTable.show_dice(dice))
        return dice
