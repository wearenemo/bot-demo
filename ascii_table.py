from utils import Text as T


class AsciiTable:
    """
       ===============
      |               |
      |               |
     □|               |□
      |     CRAPPY    |
      |     CASINO    |
     □|               |□
      |               |
      |               |
     X|               |□
      |               |
      |               |
     □|               |□
      |     CRAPPY    |
      |     CASINO    |
     □|               |9
      |               |
      |               |
       ===============
    """

    top_bottom_row = [
        '      ==============      ',
    ]
    casino_row = [
        '     |    CRAPPY    |     ',
        '     |    CASINO    |     '
    ]

    empty_chair_row = [
        '   _ |              | _   ',
    ]

    dead_row = [
        '     |              |     ',
    ]

    dealer_row = [
        '     |--            |     ',
        '   ● |D |   CC      | _   ',
        '     |--            |     ',
    ]

    table = top_bottom_row + \
            dead_row + \
            dead_row + \
            empty_chair_row + \
            casino_row + \
            empty_chair_row + \
            dead_row + \
            dealer_row + \
            dead_row + \
            empty_chair_row + \
            casino_row + \
            empty_chair_row + \
            dead_row + \
            dead_row + \
            top_bottom_row

    button = '●'

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

    left_seats  = [0, 2, 5, 7]
    right_seats = [1, 3, 4, 6, 8]

    @classmethod
    def empty(cls):
        return T.mono('\n'.join(cls.table))

    @classmethod
    def from_table(cls, table, include_players=True):
        ascii_table = AsciiTable.empty()
        last_idx = 0
        player_str = ""
        P = 1
        empty_seats = []
        for i, s in enumerate(table.seats):
            t_idx = ascii_table.find('_', last_idx + 1)
            last_idx = t_idx
            if s.occupied:
                b = ' '
                if table.button_position == i:
                    b = cls.button
                if i in cls.left_seats:
                    replacement = f'   {str(P)} |{b}'
                else:
                    replacement = f'{b}| {str(P)}   '
                ascii_table = (
                    f'{ascii_table[:t_idx - 3]}'
                    f'{replacement}'
                    f'{ascii_table[t_idx + 4:]}'
                )
                player_str += (
                    f'\n {P} -'
                    f' {s.player.name} '
                    f'[${s.player.coins:.0f}]'
                )
                P += 1
            else:
                empty_seats.append(i + 1)
        if table.point:
            ascii_table = ascii_table.replace("CC", f'{table.point:2.0f}')
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
            s += f'  {d1_row}   {d2_row}\n'
        return T.mono(s)
