import hashlib
import sys

BUFFER_SIZE = 4 * 1024 # how much data to read at once

def hash_stream(reader):
    sha256 = hashlib.sha256()
    while True:
        block = reader.read(BUFFER_SIZE)
        if not block:
            break
        sha256.update(block)
    return sha256.hexdigest()

if __name__ == "__main__":
    reader = open(sys.argv[1], "rb")
    result = hash_stream(reader)
    print(result)
