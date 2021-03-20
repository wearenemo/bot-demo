from game.table import Table
from game.exceptions import AlreadyExists


class CrapsManager:
    def __init__(self):
        self._tables = {}

    def table_for(self, id):
        return self._tables.get(id)

    def create_table(self, num_seats, _id, dealer_delegate):
        if _id in self._tables:
            raise AlreadyExists('table already exists')
        table = Table(num_seats, _id, dealer_delegate)
        self._tables[_id] = table
        return table
