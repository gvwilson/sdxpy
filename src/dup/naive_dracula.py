from collections import Counter
import plotly.express as px
import plotly.io as pio
from naive_hash import naive_hash

def plot(stem, counts):
    x = list(counts.keys())
    y = list(counts.values())
    fig = px.bar(
        {"hash": x, "count": y},
        x="hash", y="count",
        color_discrete_sequence=["gray"],
        template="plotly_white"
    )
    fig.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0})
    fig.write_image(f"{stem}.svg", height=300)
    fig.write_image(f"{stem}.pdf", height=300)

pio.kaleido.scope.mathjax = None

lines = [bytes(ln.strip(), "utf-8") for ln in open("dracula.txt", "r").readlines()]
plot("naive_dracula", Counter(naive_hash(ln) for ln in lines))

unique = set(lines)
plot("naive_dracula_unique", Counter(naive_hash(ln) for ln in unique))
