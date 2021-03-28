import asyncio
from datetime import datetime as dt
import random

from bot.exceptions import SceneException

from utils import Emoji as E
from utils import Text as T

from game.dice import Dice
from ascii_table import AsciiTable


class GetRollScene:

    ROLL_CMDS = ['roll', 'dice']
    BLOW_CMDS = ['blow', E.BLOW]

    # Banter is said right after the player 'roll's
    dice_out = [
        "Dice are out!",
        "Dice are loose!",
        "Dice are live!",
        "Dice are hot!",
    ]

    def dice_out(self):
        out = random.choice(['out', 'loose', 'live', 'hot'])
        dice = random.choice(["Dice", "The dice"])
        return f"{dice} are {out}!"

    def state_point(self, point):
        if point is None:
            return ""
        ps = f'{point:.0f}'
        return random.choice([
            f" Point is {ps}.",
            f" The point is {ps}.",
            f" Point's {ps}.",
        ])

    def preface(self, point):
        return f'{self.dice_out()}{self.state_point(point)}'

    generic_banter = [
        "Winner winner, chicken dinner!",
        "Let's get rich!",
        "Show me something good!",
        "The best things in life are free. But not the best things in Vegas.",
        "Daddy needs a new pair of shoes!",
    ]

    generic_prepoint = [
        "Looking for a natural 7 or 11!",
        "Am I stoned and 16 again? Because I really want 7/11...",
        "No craps no craps no craps!",
        "Coming out!",
        "Sometimes I wonder... maybe there just *isn't* a point.",
    ]

    generic_postpoint = [
        f"Anything but seven!",
        f"Not a seven? I'm in heaven!",
    ]

    banter_for_point = {
        4: [
            "May the FOUR be with you!",
            "Duecey-duecey, always juicy!"
        ],
        5: [
            "2 and 3 or 4 and 1, that's the way we get it done!",
            "Look alive! We need a five!",
        ],
        6: [
            "Six was always the best number if you ask me.",
            "Did I tell you about the time I *became* six?",
        ],
        8: [
            "Eights always seemed easy to me.",
            "Eights are considered very lucky in some cultures.",
        ],
        9: [
            "Why was six afraid of seven?",
            "Not in time? Press star six nine!",
        ],
        10: [
            "Tens are tough, but you're tougher.",
            "Honestly, I don't have a good feeling about this roll.",
        ],
        11: [
            "YO eleven! YO good field! Show me a five and a six!",
            "Five and six will do the trick!",
        ],
    }

    def banter(self, point, thrown_by_player):
        options = self.generic_banter[:]
        if point is None:
            # twice as likely to get the more specific banter
            options.extend(self.generic_prepoint[:])
            options.extend(self.generic_prepoint[:])
        else:
            # postpoint banter is a bit more interesting
            options.extend(self.generic_postpoint[:])
            options.extend(self.generic_postpoint[:])

            # handle 4, 6, 8, 10 a little specially
            if point % 2 == 0:
                half = f'{point / 2:.0f}'
                options.append(f"Wouldn't mind a couple {half}'s right now!")
                options.append(f"A pair of {half}'s would be fine by me!")

            ps = f'{point:.0f}'
            generic_for_point = [
                f"Come on, show me {ps}!",
                f"I once knew a guy who only rolled {ps}'s. Too bad he's not here.",
            ]
            options.extend(generic_for_point[:])
            options.extend(generic_for_point[:])
            specific = self.banter_for_point.get(point, [])

            # point-specific banter is 3x more likely than base generic
            options.extend(specific)
            options.extend(specific)
            options.extend(specific)
        preface = self.preface(point)
        option = f'{random.choice(options)}'
        if not thrown_by_player:
            option = ""
        else:
            option = f'\n{T.block_quote(option)}'
        return f'{T.bold(preface)}{option}'

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
        self.nap = 0.4
        self.leave_dice_for = 2.0
        if bot.TEST_MODE or table.empty:
            self.timeout = 2.0
            self.roll_duration = 0.0
            self.nap = 0.1
            self.leave_dice_for = 1.0
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

            # full banter only happens when the player initiates the roll.
            banter = self.banter(table.point, True)
            await display_channel.send(banter)

        except asyncio.TimeoutError:
            async with display_channel.typing():
                await waiting.add_reaction(E.HOURGLASS)
                await asyncio.sleep(self.nap)
                new_content = waiting.content + " nevermind, I can do it for you."
                await waiting.edit(content=new_content)
            await asyncio.sleep(self.nap)
            banter = self.banter(table.point, False)
            await display_channel.send(banter)
        finally:
            await asyncio.sleep(3 * self.nap)
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
        vals = dice.values
        e0 = E.for_number(vals[0])
        e1 = E.for_number(vals[1])
        await roll_m.add_reaction(e0)
        if e0 != e1:
            await roll_m.add_reaction(e1)
        else:
            # doubles
            await roll_m.add_reaction(E.MULTIPLY)
            await roll_m.add_reaction(E.TWO)
        await asyncio.sleep(self.leave_dice_for)
        return dice
