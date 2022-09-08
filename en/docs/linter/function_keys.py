def label():
    return "label"

actually_has_duplicate_keys = {
    "label": 1,
    "la" + "bel": 2,
    label(): 3,
    "".join(["l", "a", "b", "e", "l"]): 4
}
