"""A column-oriented dataframe."""

import inspect

# [top]
from df_base import DF
from util import all_eq


class DfCol(DF):
    """Column-wise dataframe."""

    def __init__(self, **kwargs):
        """Initialize from `name=[values]`."""
        assert len(kwargs) > 0
        assert all_eq(len(kwargs[k]) for k in kwargs)
        for k in kwargs:
            assert all_eq(type(v) for v in kwargs[k])
        self._data = kwargs

    # [/top]

    # [simple]
    def ncol(self):
        """Report the number of columns."""
        return len(self._data)

    def nrow(self):
        """Report the number of rows."""
        n = set(self._data.keys()).pop()
        return len(self._data[n])

    def cols(self):
        """Return the set of column names."""
        return set(self._data.keys())

    # [/simple]

    # [eq]
    def eq(self, other):
        """Check equality of two dataframes."""
        assert isinstance(other, DF)
        for n in self._data:
            if n not in other.cols():
                return False
            for i in range(len(self._data[n])):
                if self.get(n, i) != other.get(n, i):
                    return False
        return True

    # [/eq]

    # [get]
    def get(self, col, row):
        """Get a scalar value."""
        assert col in self._data
        assert 0 <= row < len(self._data[col])
        return self._data[col][row]

    # [/get]

    # [select]
    def select(self, *names):
        """Select a subset of columns."""
        assert all(n in self._data for n in names)
        return DfCol(**{n: self._data[n] for n in names})

    # [/select]

    # [filter]
    def filter(self, func):
        """Select a subset of rows."""
        params = list(inspect.signature(func).parameters.keys())
        result = {n: [] for n in self._data}
        for i in range(self.nrow()):
            args = {n: self._data[n][i] for n in self._data}
            if func(**args):
                for n in self._data:
                    result[n].append(self._data[n][i])
        return DfCol(**result)

    # [/filter]

    def __str__(self):
        return str(self._data)
