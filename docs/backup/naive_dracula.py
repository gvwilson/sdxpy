from collections import Counter
import plotly.express as px
from naive_hash import naive_hash

lines = open("dracula.txt", "r").readlines()
hashes = [naive_hash(ln) for ln in lines]
counts = Counter(hashes)
print("hash,count")
x, y = [], []
for (h, c) in sorted(counts.items()):
    x.append(h)
    y.append(c)
    print(f"{h},{c}")

fig = px.bar({"hash": x, "count": y}, x="hash", y="count")
fig.write_image("naive_dracula.svg")
