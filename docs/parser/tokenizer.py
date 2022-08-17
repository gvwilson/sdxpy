SIMPLE = {
  "*": "Any",
  "|": "Alt",
  "(": "GroupStart",
  ")": "GroupEnd"
}

# [tokenize]
def tokenize(text):
    result = []
    for (i, c) in enumerate(text):
        if c in SIMPLE:
            result.append({"kind": SIMPLE[c], "loc": i})
        elif (c == "^") and (i == 0):
            result.append({"kind": "Start", "loc": i})
        elif (c == "$") and (i == (len(text) - 1)):
            result.append({"kind": "End", "loc": i})
        else:
            result.append({"kind": "Lit", "loc": i, "value": c})
    return result
# [/tokenize]
