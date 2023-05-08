import csv
from glob import glob
import sys
from pathlib import Path
from hashlib import sha256

# [func]
HASH_LEN = 16

def hash_all(root):
    result = []
    for name in glob("**/*.*", root_dir=root, recursive=True):
        full_name = Path(root, name)
        with open(full_name, "rb") as reader:
            data = reader.read()
            hash_code = sha256(data).hexdigest()[:HASH_LEN]
            result.append((name, hash_code))
    return result
# [/func]

if __name__ == "__main__":
    root = sys.argv[1]
    table = hash_all(root)
    writer = csv.writer(sys.stdout)
    writer.writerow(["filename", "hash"])
    writer.writerows(table)
