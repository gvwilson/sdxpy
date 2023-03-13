import json

from tokenizer_collapse import tokenize

test = "ab*"
result = tokenize(test)
print(test, "=>", json.dumps(result, indent=2))
