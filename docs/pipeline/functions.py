import csv

def read(filename):
    with open(filename, "r") as reader:
        return [row for row in csv.reader(reader)]

def head(data, num):
    return data[:num]

def tail(data, num):
    return data[-num:]

def left(data, num):
    return [r[:num] for r in data]

def right(data, num):
    return [r[-num:] for r in data]
