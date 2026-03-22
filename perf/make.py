from pprint import pprint
from timing import make_col, make_row

col = make_col(3, 3)
print("column-wise")
pprint(col._data)

print()

row = make_row(3, 3)
print("row-wise")
pprint(row._data)
