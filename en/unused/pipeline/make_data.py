import csv
import sys

assert len(sys.argv) == 3, f"Usage: {sys.argv[0]} rows columns"
rows = int(sys.argv[1])
cols = int(sys.argv[2])

writer = csv.writer(sys.stdout)
for r in range(rows):
    writer.writerow([f" {r+1:02d}x{c+1:02d}" for c in range(cols)])
