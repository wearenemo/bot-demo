from game.table import Table
from game.exceptions import AlreadyExists
from game.dealer_delegate import DealerDelegate


class CrapsManager:
    def __init__(self):
        self._tables = {}

    def table_for(self, _id: int):
        print('getting table with id', _id)
        return self._tables.get(_id)

    def create_table(self,
                     num_seats: int,
                     _id: int,
                     dealer_delegate: DealerDelegate):
        print('creating table with id', _id)
        if _id in self._tables:
            raise AlreadyExists('table already exists')
        table = Table(num_seats, _id, dealer_delegate)
        self._tables[_id] = table
        return table
