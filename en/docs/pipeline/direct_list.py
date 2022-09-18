from functions import *

pipeline = [[read, "sample_data.csv"], [head, 10], [tail, 5], [left, 2]]

for (i, step) in enumerate(pipeline):
    func, params = step[0], step[1:]
    if i == 0:
        data = func(*params)
    else:
        data = func(data, *params)

# [omit]
import csv
import sys

csv.writer(sys.stdout).writerows(data)
# [/omit]
