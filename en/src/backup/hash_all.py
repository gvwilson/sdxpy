import csv
import glob
import sys
from pathlib import Path

from hash_stream import hash_stream

def hash_all(root_dir):
    result = []
    for filename in glob.glob("**/*.*", root_dir=root_dir, recursive=True):
        full_name = Path(root_dir, filename)
        with open(full_name, "rb") as reader:
            hash_code = hash_stream(reader)
            result.append((filename, hash_code))
    return result

if __name__ == "__main__":
    root_dir = sys.argv[1]
    table = hash_all(root_dir)
    writer = csv.writer(sys.stdout)
    writer.writerow(["filename", "hash"])
    writer.writerows(table)
