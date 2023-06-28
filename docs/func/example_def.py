# [python]
def same(num):
    return num
# [/python]

# [def]
["func", ["num"], ["get", "num"]]
# [/def]

# [save]
["set", "same", ["func", ["num"], ["get", "num"]]]
# [/save]

# [lambda]
double = lambda x: 2 * x
double(3)
# [/lambda]

# [call]
["call", "same", 3]
# [/call]
