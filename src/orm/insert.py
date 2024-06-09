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
        self._names = [m['name'] for m in self._meta]

    def insert(self, thing):
        values = self._get_values(thing)
        colnames = ', '.join(m['name'] for m in self._meta)
        stmt = f'insert into {self._table_name()}({colnames}) values({values})'
        print(stmt)
        self._conn.execute(stmt)
        self._conn.commit()

    def _get_values(self, thing):
        assert len(thing) == len(self._meta)
        if isinstance(thing, list) or isinstance(thing, tuple):
            assert all(isinstance(v, m['type']) for (v, m) in zip(thing, self._meta))
            values = list(thing)
        elif isinstance(thing, dict):
            assert all(k in self._names for k in thing.keys())
            assert all(isinstance(thing[k], self._meta[k]['type']) for k in thing.keys())
            values = [thing[m['name']] for m in self._meta]
        return ', '.join(repr(v) if isinstance(v, str) else str(v) for v in values)

    def _table_name(self):
        return self.__class__.__name__


class Person(ORM):
    pass


def main():
    connection = sqlite3.connect(sys.argv[1])
    p = Person(connection)
    p.insert([55, 'Terese', 'DiOrio'])


if __name__ == '__main__':
    main()
