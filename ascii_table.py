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
    table = [
        '      ===============      ',
        '     | ♠   ♡   ♣   ♢ |     ',
        '     |               |     ',
        '   2 |               | 3   ',
        '     |    CRAPPY♤    |     ',
        '     |    ♡CASINO    |     ',
        '   1 |               | 4   ',
        '     |               |     ',
        '     |--             |     ',
        '   ● |D |            | 5   ',
        '     |--             |     ',
        '     |               |     ',
        '   9 |               | 6   ',
        '     |     ~~~~~     |     ',
        '     |    | OFF |    |     ',
        '   8 |     ~~~~~     | 7   ',
        '     |               |     ',
        '     | ♤   ♥   ♧   ♦ |     ',
        '      ===============      '
    ]

    little_dice = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']

    dice = {
        1: [
            ' _____ ',
            '|     |',
            '|  ●  |',
            '|     |',
            ' ‾‾‾‾‾ '
        ],
        2: [
            ' _____ ',
            '|    ●|',
            '|     |',
            '|●    |',
            ' ‾‾‾‾‾ '
        ],
        3: [
            ' _____ ',
            '|    ●|',
            '|  ●  |',
            '|●    |',
            ' ‾‾‾‾‾ '
        ],
        4: [
            ' _____ ',
            '|●   ●|',
            '|     |',
            '|●   ●|',
            ' ‾‾‾‾‾ '
        ],
        5: [
            ' _____ ',
            '|●   ●|',
            '|  ●  |',
            '|●   ●|',
            ' ‾‾‾‾‾ '
        ],
        6: [
            ' _____ ',
            '|●   ●|',
            '|●   ●|',
            '|●   ●|',
            ' ‾‾‾‾‾ '
        ],
        None: [
            ' _____ ',
            '|     |',
            '|  ?  |',
            '|     |',
            ' ‾‾‾‾‾ '
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
        b_idx = ascii_table.find(str(btn_idx))

        # let's use the 3 die for now
        button = cls.little_dice[2]

        if btn_idx in cls.left_seats:
            b_idx += 3
        else:
            b_idx -= 3
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
                player_str += (
                    f'\n {p} -'
                    f' {s.player.name} '
                    f'[${s.player.coins:.0f}]'
                )
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
            ascii_table += T.bold(seats_str) + f'{T.mono(player_str)}'
        return ascii_table

    @classmethod
    def show_dice(cls, dice):
        d1 = cls.dice[dice.values[0]]
        d2 = cls.dice[dice.values[1]]
        s = ""
        for d1_row, d2_row in zip(d1, d2):
            s += f'     {d1_row}   {d2_row}\n'
        return T.mono(s)
