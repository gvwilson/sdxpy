from tokenizer import tokenize

def parse(text):
    result = []
    all_tokens = tokenize(text)
    for (i, token) in enumerate(all_tokens):
        is_last = i == len(all_tokens) - 1
        handle(result, token, is_last)
    return compress(result)

# [skip]
# [handle]
def handle(result, token, is_last):
    if token["kind"] == "Lit":
        result.append(token)
    elif token["kind"] == "Start":
        assert len(result) == 0, "Should not have start token after other tokens"
        result.append(token)
    elif token["kind"] == "End":
        assert is_last, "Should not have end token before other tokens"
        result.append(token)
    elif token["kind"] == "GroupStart":
        result.append(token)
    elif token["kind"] == "GroupEnd":
        result.append(group_end(result, token))
    elif token["kind"] == "Any":
        assert len(result) > 0, f'No operand for "*" ({token["loc"]})'
        token["child"] = result.pop()
        result.append(token)
    elif token["kind"] == "Alt":
        assert len(result) > 0, f'No operand for "|" ({token["loc"]})'
        token["left"] = result.pop()
        token["right"] = None
        result.append(token)
    else:
        assert False, f'UNIMPLEMENTED {token["kind"]}'
# [/handle]

# [groupend]
def group_end(result, token):
    group = {"kind": "Group", "loc": None, "end": token["loc"], "children": []}
    while True:
        assert len(result) > 0, f'Unmatched end parenthesis ({token["loc"]})'
        child = result.pop()
        if child["kind"] == "GroupStart":
            group["loc"] = child["loc"]
            break
        group["children"].insert(0, child)
    return group
# [/groupend]

# [compress]
def compress(raw):
    cooked = []
    while len(raw) > 0:
        token = raw.pop()
        if token["kind"] == "Alt":
            assert len(cooked) > 0, f'No right operand for alt ({token["loc"]})'
            token["right"] = cooked.pop(0)
        cooked.insert(0, token)
    return cooked
# [/compress]
# [/skip]
