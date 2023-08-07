class DataFrame:
    def ncol(self):
        """Report the number of columns."""

    def nrow(self):
        """Report the number of rows."""

    def cols(self):
        """Return the set of column names."""

    def eq(self, other):
        """Check equality with another dataframe."""

    def get(self, col, row):
        """Get a scalar value."""

    def select(self, *names):
        """Select a named subset of columns."""

    def filter(self, func):
        """Select a subset of rows by testing values."""
