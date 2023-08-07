import pandas as pd
import plotly.express as px
import plotly.io as pio

pio.kaleido.scope.mathjax = None

df = pd.read_csv("timing.csv")
df["ncell"] = df["nrow"] * df["ncol"]
for new, old in [
        ["f_col", "filter_col"],
        ["s_col", "select_col"],
        ["f_row", "filter_row"],
        ["s_row", "select_row"]]:
    df[new] = df[old] / df["ncell"]

stats = df[["f_col", "s_col", "f_row", "s_row"]].agg("mean")

def ratio(pct):
    c = (pct * stats["f_col"]) + ((1 - pct) * stats["s_col"])
    r = (pct * stats["f_row"]) + ((1 - pct) * stats["s_row"])
    return c / r

percentages = list(range(0, 101, 10))
ratios = [ratio(p / 100) for p in percentages]
temp = pd.DataFrame({"percentage": percentages, "ratio": ratios})
fig = px.line(temp, x="percentage", y="ratio",
              labels={
                  "percentage": "percentage of filter operations (vs. select)",
                  "ratio": "ratio of column-wise time to row-wise time"
              },
              color_discrete_sequence=["gray"],
              template="plotly_white")

fig.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0})
fig.write_image("analysis.pdf", width="620", height="400")
fig.write_image("analysis.svg", width="620", height="400")
