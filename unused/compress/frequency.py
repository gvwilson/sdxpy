from collections import Counter
import plotly.express as px
import re
import sys


def main(text, stem):
    """Calculate token frequency."""
    counts = Counter(t for t in re.split(r'\b', text) if len(t) > 0)
    rows = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
    freq = Counter(r[1] for r in rows)
    freq = sorted(freq.items(), key=lambda pair: pair[0], reverse=True)
    num_occ = [p[0] for p in freq]
    num_items = [p[1] for p in freq]
    fig = px.line(
        {"occurrences": num_occ, "log(count)": num_items},
        x="occurrences", y="log(count)",
        log_x=True,
        log_y=True,
        markers=True,
        color_discrete_sequence=["gray"],
        template="plotly_white"
    )
    fig.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0})
    fig.write_image(f"{stem}.svg", height=300)
    fig.write_image(f"{stem}.pdf", height=300)



if __name__ == "__main__":
    main(sys.stdin.read(), sys.argv[1])
