import sqlite3
import sys

class ORM:
    def __init__(self, connection):
        self._conn = connection
        self._conn.row_factory = sqlite3.Row

    def select(self, *columns):
        query = self._build_sql(columns)
        return [
            dict(row)
            for row in self._conn.execute(query).fetchall()
        ]

    def _build_sql(self, columns):
        if columns:
            cols = ', '.join(columns)
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
    print('all')
    for row in p.select():
        print(row)
    print('family name')
    for row in p.select('family'):
        print(row)


if __name__ == '__main__':
    main()
