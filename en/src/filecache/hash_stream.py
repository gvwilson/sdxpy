import hashlib
import sys

BUFFER_SIZE = 4 * 1024 # how much data to read at once

def hash_stream(reader):
    hasher = hashlib.md5()
    while True:
        block = reader.read(BUFFER_SIZE)
        if not block:
            break
        hasher.update(block)
    return hasher.hexdigest()

if __name__ == "__main__":
    reader = open(sys.argv[1], "rb")
    result = hash_stream(reader)
    print(result)
