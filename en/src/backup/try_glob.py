import glob
import sys

root_dir = sys.argv[1]
for filename in glob.glob("**/*.*", root_dir=root_dir, recursive=True):
    print(filename)
