SIMPLE = {
  "*": "Any",
  "|": "Alt",
  "(": "GroupStart",
  ")": "GroupEnd"
}

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
            combine_or_push(result, c, i)
    return result

# [combine]
def combine_or_push(so_far, character, location):
  if (len(so_far) == 0) or (so_far[-1]["kind"] != "Lit"):
      so_far.append({"kind": "Lit", "value": character, "loc": location})
  else:
      so_far[-1]["value"] += character
# [/combine]
