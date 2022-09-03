import csv

EXPORTS = {}

def export(func):
    global EXPORTS
    EXPORTS[func.__name__] = func
    return func

# [sample]
@export
def read(filename, **kwargs):
    with open(filename, "r") as reader:
        return [row for row in csv.reader(reader)]

@export
def head(data, num, **kwargs):
    return data[:num]
# [/sample]

@export
def tail(data, num, **kwargs):
    return data[-num:]

@export
def left(data, num, **kwargs):
    return [r[:num] for r in data]

@export
def right(data, num, **kwargs):
    return [r[-num:] for r in data]
