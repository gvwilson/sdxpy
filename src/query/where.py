import sqlite3
import sys

class Binary:
    def __init__(self, op, left, right):
        self._op = op
        self._left = left
        self._right = right

    def __str__(self):
        left = self._as_str(self._left)
        right = self._as_str(self._right)
        return f'({left} {self._op} {right})'

    def _as_str(self, thing):
        if isinstance(thing, str):
            return repr(thing)
        return str(thing)


class Col:
    def __init__(self, name):
        self._name = name

    def __eq__(self, other):
        return Binary('=', self, other)

    def __gt__(self, other):
        return Binary('>', self, other)

    def __str__(self):
        return self._name


class ORM:
    def __init__(self, connection, verbose=False):
        self._conn = connection
        self._conn.row_factory = sqlite3.Row
        self._columns = None
        self._conds = None
        self._verbose = verbose

    def run(self):
        query = self._build_sql()
        if self._verbose:
            print(query)
        return [
            dict(row)
            for row in self._conn.execute(query).fetchall()
        ]

    def select(self, *columns):
        if columns:
            self._columns = list(columns)
        return self

    def where(self, *conditions):
        assert conditions
        self._conds = list(conditions)
        return self

    def _build_sql(self):
        cols = ', '.join(self._columns) if self._columns else '*'
        if self._conds:
            where = f'where {" and ".join(str(c) for c in self._conds)}'
        else:
            where = ''
        return f'select {cols} from {self._table_name()} {where}'

    def _table_name(self):
        return self.__class__.__name__


class Person(ORM):
    pass


def main():
    connection = sqlite3.connect(sys.argv[1])
    p = Person(connection, verbose=True)
    for row in p.select('family', 'personal').where(Col('family') > 'S').run():
        print(row)


if __name__ == '__main__':
    main()
