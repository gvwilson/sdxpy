from collections import Counter
from hashlib import sha256
import plotly.express as px

lines = {ln.strip() for ln in open("dracula.txt", "r").readlines()}
hashes = [sha256(bytes(ln, "utf-8")).hexdigest() for ln in lines]
counts = Counter(hashes)
print(len(set(counts.values())))

counts = Counter(int(h, 16) % 20 for h in hashes)
x = list(counts.keys())
y = list(counts.values())
fig = px.bar({"hash": x, "count": y}, x="hash", y="count")
fig.write_image("sha256_dracula.svg")
fig.write_image("sha256_dracula.pdf")
