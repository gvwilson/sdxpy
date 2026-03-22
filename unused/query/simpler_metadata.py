import sqlite3
import sys

class ORM:
    def __init__(self, connection):
        self._conn = connection
        self._conn.row_factory = sqlite3.Row

    def select(self):
        query = f'select * from {self._table_name()}'
        return [
            dict(row)
            for row in self._conn.execute(query).fetchall()
        ]

    def _table_name(self):
        return self.__class__.__name__


class Person(ORM):
    pass


def main():
    connection = sqlite3.connect(sys.argv[1])
    p = Person(connection)
    for row in p.select():
        print(row)


if __name__ == '__main__':
    main()
