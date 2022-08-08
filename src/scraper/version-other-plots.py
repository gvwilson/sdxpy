import sys
import pandas as pd
import plotly.express as px

datafile = sys.argv[1]
packages = pd.read_csv(datafile)
slice = packages[packages['Releases'] < 100]

fig = px.violin(slice, y='Releases')
fig.show()
fig.write_image('figures/release-count-violin.svg', width=600, height=400)

#--------

fig = px.box(slice, y='Releases')
fig.show()
fig.write_image('figures/release-count-box.svg', width=600, height=400)
