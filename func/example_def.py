# mccole:python
def same(num):
    return num
# mccole:/python

# mccole:def
["func", ["num"], ["get", "num"]]
# mccole:/def

# mccole:save
["set", "same", ["func", ["num"], ["get", "num"]]]
# mccole:/save

# mccole:lambda
double = lambda x: 2 * x
double(3)
# mccole:/lambda

# mccole:call
["call", "same", 3]
# mccole:/call
