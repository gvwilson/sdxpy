#!/usr/bin/env python

import sys
import pandas as pd
import plotly.express as px

df = pd.read_csv(sys.argv[1])
fig = px.line(df, x="date", y="words")
fig.show()
