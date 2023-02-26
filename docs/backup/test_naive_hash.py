from naive_hash import naive_hash

sample = "abcdefg"
for i in range(2, len(sample) + 1):
    slice = sample[:i]
    hash = naive_hash(slice)
    print(f"{hash:2}: slice")
