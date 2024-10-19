import sqlite3
import sys

class ORM:
    TRANSLATE = {
        'INTEGER': int,
        'TEXT': str,
    }

    def __init__(self, connection):
        self._conn = connection
        pragma = f'PRAGMA table_info({self._table_name()})'
        self._meta = [
            {
                'name': row[1],
                'type': ORM.TRANSLATE[row[2]],
                'nullable': bool(row[3]),
                'primary_key': bool(row[5]),
            }
            for row in self._conn.execute(pragma).fetchall()
        ]

    def select(self):
        query = f'select * from {self._table_name()}'
        return [
            {
                self._meta[i]['name']: val
                for i, val in enumerate(row)
            }
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
