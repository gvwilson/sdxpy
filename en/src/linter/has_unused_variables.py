used = 3
distractor = 2
not_used = used + distractor

def no_unused(param):
    result = 2 * param
    return result

def has_unused(param):
    used = 3 * param
    not_used = 2 * param
    distractor = "distraction"
    return used
