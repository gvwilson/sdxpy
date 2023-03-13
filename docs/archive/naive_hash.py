def naive_hash(text):
    result = 0
    for ch in text:
        result = ((result * 13) + ord(ch)) % 17
    return result
