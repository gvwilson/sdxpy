import sys
from naive_hash import naive_hash


def same_bytes(left_name, right_name):
  left_file = open(left_name, "rb")
  left_bytes = left_name.read()

  right_file = open(right_name, "rb")
  right_bytes = right_name.read()

  left_file.close()
  right_file.close()
  
  return left_bytes == right_bytes


def find_duplicates(filenames):
    matches = []
    for i_left in range(len(filenames)):
        left = filenames[i_left]
        for i_right in range(i_left):
            right = filenames[i_right]
            if same_bytes(left, right):
                matches.append((left, right))
    return matches


# [group]
def find_groups(filenames):
    groups = {}
    for fn in filenames:
        data = open(fn, "rb").read()
        hash_code = naive_hash(data)
        if hash_code not in groups:
            groups[hash_code] = set()
        groups[hash_code].add(fn)
    return groups
# [/group]


if __name__ == "__main__":
    # [main]
    groups = find_groups(sys.argv[1:])
    for filenames in groups.values():
        duplicates = find_duplicates(list(filenames))
        for (left, right) in duplicates:
            print(left, right)
    # [/main]
