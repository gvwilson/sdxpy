import glob
import sys

root = sys.argv[1]
for name in glob.glob("**/*.txt", root_dir=root, recursive=True):
    print(name)
