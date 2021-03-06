from utils import Text as T


class AsciiTable:
    """
        ==============
       |              |
       |              |
       |              |
       |    CRAPPY    |
       |    CASINO    |
     1 |●             |
       |              |
       |--            |
     ● |D |    8      |
       |--            |
       |              |
       |              |
       |    CRAPPY    |
       |    CASINO    |
       |              |
       |              |
       |              |
        ==============
    """

    CHIP = '$'

    table = [
        '     ┏━━━━━━━━━━━━━━━┓     ',
        '     ┃ ♠   ♡   ♣   ♢ ┃     ',
        '     ┠─┬─┬───────┬─┬─┨     ',
        '   2 ┃ │ │       │ │ ┃ 3   ',
        '     ┃ │ │ℂRAPPY♤│ │ ┃     ',
        '     ┃ │ │♡ℂASINO│ │ ┃     ',
        '   1 ┃ │ │       │ │ ┃ 4   ',
        '     ┃ │ │       │ │ ┃     ',
        '     ┠─┴╮│       │ │ ┃     ',
        '   ● ┃  ││       │ │ ┃ 5   ',
        '     ┠─┬╯│       │ │ ┃     ',
        '     ┃ │ │       │ │ ┃     ',
        '   9 ┃ │ │       │ │ ┃ 6   ',
        '     ┃ │ │╔═════╗│ │ ┃     ',
        '     ┃ │ │║ OFF ║│ │ ┃     ',
        '   8 ┃ │ │╚═════╝│ │ ┃ 7   ',
        '     ┠─┴─┴───────┴─┴─┨     ',
        '     ┃ ♤   ♥   ♧   ♦ ┃     ',
        '     ┗━━━━━━━━━━━━━━━┛     '
    ]

    little_dice = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']

    dice = {
        1: [
            '┏━━━━━━━┓',
            '┃       ┃',
            '┃   ●   ┃',
            '┃       ┃',
            '┗━━━━━━━┛'
        ],
        2: [
            '┏━━━━━━━┓',
            '┃     ● ┃',
            '┃       ┃',
            '┃ ●     ┃',
            '┗━━━━━━━┛'
        ],
        3: [
            '┏━━━━━━━┓',
            '┃     ● ┃',
            '┃   ●   ┃',
            '┃ ●     ┃',
            '┗━━━━━━━┛'
        ],
        4: [
            '┏━━━━━━━┓',
            '┃ ●   ● ┃',
            '┃       ┃',
            '┃ ●   ● ┃',
            '┗━━━━━━━┛'
        ],
        5: [
            '┏━━━━━━━┓',
            '┃ ●   ● ┃',
            '┃   ●   ┃',
            '┃ ●   ● ┃',
            '┗━━━━━━━┛'
        ],
        6: [
            '┏━━━━━━━┓',
            '┃ ●   ● ┃',
            '┃ ●   ● ┃',
            '┃ ●   ● ┃',
            '┗━━━━━━━┛'
        ],
        None: [
            '┏━━━━━━━┓',
            '┃       ┃',
            '┃   ?   ┃',
            '┃       ┃',
            '┗━━━━━━━┛'
        ]
    }

    left_seats  = [1, 2, 8, 9]
    right_seats = [3, 4, 5, 6, 7]

    @classmethod
    def empty(cls):
        return T.mono('\n'.join(cls.table))

    @classmethod
    def from_table(cls, table, include_players=True):
        ascii_table = AsciiTable.empty()
        btn_idx = table.button_position + 1
        if not table.empty:
            b_idx = ascii_table.find(str(btn_idx))
            if btn_idx in cls.left_seats:
                b_idx += 1
            else:
                b_idx -= 1
        else:
            # dealer gets button
            b_idx = ascii_table.find('●')
            b_idx += 1

        # let's use the 3 die for now
        button = cls.little_dice[2]

        ascii_table = (
            f'{ascii_table[:b_idx]}'
            f'{button}'
            f'{ascii_table[b_idx + 1:]}')

        player_str = ""
        empty_seats = []
        for s in table.seats:
            i = s.index + 1
            p = ' '
            if s.occupied:
                p = f'{i:.0f}'
                # add chips to pass line
                if s.player.has_pass_bet:
                    p_idx = ascii_table.find(p)
                    if i in cls.left_seats:
                        chip_idx = p_idx + 3
                    else:
                        chip_idx = p_idx - 3
                    ascii_table = (
                        f'{ascii_table[:chip_idx]}'
                        f'{cls.CHIP}'
                        f'{ascii_table[chip_idx + 1:]}')
                # add chips to don't pass line
                if s.player.has_no_pass_bet:
                    p_idx = ascii_table.find(p)
                    if i in cls.left_seats:
                        chip_idx = p_idx + 5
                    else:
                        chip_idx = p_idx - 5
                    ascii_table = (
                        f'{ascii_table[:chip_idx]}'
                        f'{cls.CHIP}'
                        f'{ascii_table[chip_idx + 1:]}')
                coin_str = f'[${s.player.coins:.0f}'
                coin_str += f'|${s.player.coins_on_table:.0f}]'
                player_str += (f'\n {p} - {str(s.player)}')
            else:
                empty_seats.append(i)

            # replace the integers in the template string either
            # with an empty space OR with the same number
            ascii_table = ascii_table.replace(str(i), p)

        if table.point:
            ascii_table = ascii_table.replace("OFF", f'{table.point:2.0f} ')

        seats_str = "\nSEATS"
        if empty_seats:
            seats_str += f' ({len(empty_seats)} empty) - place bet to sit\n'
        else:
            seats_str += f' (table is full)\n'
        if include_players:
            ascii_table += T.bold(seats_str)
            if player_str:
                ascii_table += f'{T.mono(player_str)}'
        return ascii_table

    @classmethod
    def show_dice(cls, dice):
        d1 = cls.dice[dice.values[0]]
        d2 = cls.dice[dice.values[1]]
        s = ""
        for d1_row, d2_row in zip(d1, d2):
            s += f'   {d1_row}   {d2_row}\n'
        return T.mono(s)
