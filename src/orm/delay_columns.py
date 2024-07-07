import sqlite3
import sys

class ORM:
    def __init__(self, connection):
        self._conn = connection
        self._conn.row_factory = sqlite3.Row
        self._columns = None

    def run(self):
        query = self._build_sql()
        return [
            dict(row)
            for row in self._conn.execute(query).fetchall()
        ]

    def select(self, *columns):
        if columns:
            self._columns = list(columns)
        return self

    def _build_sql(self):
        if self._columns:
            cols = ', '.join(self._columns)
            return f'select {cols} from {self._table_name()}'
        else:
            return f'select * from {self._table_name()}'

    def _table_name(self):
        return self.__class__.__name__


class Person(ORM):
    pass


def main():
    connection = sqlite3.connect(sys.argv[1])
    p = Person(connection)
    for row in p.select('family', 'personal').run():
        print(row)


if __name__ == '__main__':
    main()
