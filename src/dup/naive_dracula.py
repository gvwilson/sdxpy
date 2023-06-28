from collections import Counter
import plotly.express as px
from naive_hash import naive_hash

def plot(stem, counts):
    x = list(counts.keys())
    y = list(counts.values())
    fig = px.bar({"hash": x, "count": y}, x="hash", y="count")
    fig.write_image(f"{stem}.svg", height=300)
    fig.write_image(f"{stem}.pdf", height=300)

lines = [bytes(ln.strip(), "utf-8") for ln in open("dracula.txt", "r").readlines()]
plot("naive_dracula", Counter(naive_hash(ln) for ln in lines))

unique = set(lines)
plot("naive_dracula_unique", Counter(naive_hash(ln) for ln in unique))
