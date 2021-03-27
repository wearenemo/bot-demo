import asyncio
from datetime import datetime as dt

from bot.exceptions import SceneException

from utils import Emoji as E
from utils import Text as T

from game.dice import Dice
from ascii_table import AsciiTable


class GetRollScene:

    ROLL_CMDS = ['roll', 'dice']
    BLOW_CMDS = ['blow', E.BLOW]

    @classmethod
    def get_roll_command(cls, msg):
        content = msg.content.strip().lower()
        if any([content.startswith(cmd) for cmd in cls.ROLL_CMDS]):
            return cls.ROLL_CMDS[0]
        elif any([content.startswith(cmd) for cmd in cls.BLOW_CMDS]):
            return cls.BLOW_CMDS[0]
        else:
            return False

    async def show(
        self,
        bot,
        dice,
        shooter_id,
        table,
        first_roll,
        display_channel
    ):
        # set pace based on test mode
        self.timeout = 6.0
        self.roll_duration = 0.0
        self.nap = 0.3
        self.leave_dice_for = 1.5
        if bot.TEST_MODE or table.empty:
            self.timeout = 2.0
            self.roll_duration = 0.0
            self.nap = 0.1
            self.leave_dice_for = 1.5
        if shooter_id:
            user = await bot.fetch_user(shooter_id)
            bets_in = T.bold("Bets are IN!")
            wait_str = T.block_quote(
                f"Waiting {self.timeout:.0f} seconds for "
                f"{user.display_name} to `roll`...")
            waiting = await display_channel.send(
                f'{bets_in}\n{wait_str}'
            )
        else:
            await display_channel.send(
                f'No shooter. Auto-rolling...'
            )
            return await self.roll(dice, display_channel)

        def check(m):
            if m.author.id != shooter_id:
                return False
            return True if self.__class__.get_roll_command(m) else False

        try:
            resp = await bot.wait_for(
                'message', check=check, timeout=self.timeout)
            roll_cmd = self.__class__.get_roll_command(resp)
            if not roll_cmd:
                raise SceneException(
                    f"Unexpected roll command: {resp.content}")

            # add some extra flavor if the shooter blew on the dice
            if roll_cmd == self.__class__.BLOW_CMDS[0]:
                await resp.add_reaction(E.BLOW)
                await resp.add_reaction(E.DIE)

        except asyncio.TimeoutError:
            async with display_channel.typing():
                await waiting.add_reaction(E.HOURGLASS)
                await asyncio.sleep(self.nap)
                new_content = waiting.content + " nevermind, I can do it for you."
                await waiting.edit(content=new_content)
            await asyncio.sleep(self.nap)
        finally:
            return await self.roll(dice, display_channel)

    async def roll(self, dice, display_channel):
        start = dt.utcnow()
        now = dt.utcnow()
        new_dice = Dice(2)
        new_dice.roll()
        roll_m = await display_channel.send(AsciiTable.show_dice(new_dice))
        while (now - start).total_seconds() < self.roll_duration:
            new_dice = Dice(2)
            new_dice.roll()
            await roll_m.edit(content=AsciiTable.show_dice(new_dice))
            await asyncio.sleep(0.2)
            now = dt.utcnow()
        dice.roll()
        await roll_m.edit(content=AsciiTable.show_dice(dice))
        await roll_m.add_reaction(E.DIE)
        await asyncio.sleep(self.leave_dice_for)
        return dice
