import csv

# [decorator]
EXPORTS = {}

def export(func):
    global EXPORTS
    EXPORTS[func.__name__] = func
    return func
# [/decorator]

# [sample]
@export
def read(filename):
    with open(filename, "r") as reader:
        return [row for row in csv.reader(reader)]

@export
def head(data, num):
    return data[:num]
# [/sample]

@export
def tail(data, num):
    return data[-num:]

@export
def left(data, num):
    return [r[:num] for r in data]

@export
def right(data, num):
    return [r[-num:] for r in data]
