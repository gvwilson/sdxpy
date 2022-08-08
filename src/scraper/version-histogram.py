import sys
import pandas as pd
import plotly.express as px

datafile = sys.argv[1]
packages = pd.read_csv(datafile)

print('Distribution of Releases')
print(packages.groupby('Releases').count())
print(f'{packages["Releases"].isna().sum()} missing values')

fig = px.histogram(packages, x='Releases', nbins=100, log_y=True, width=600, height=400)
fig.show()
fig.write_image('figures/release-count.svg')

#--------

slice = packages[packages['Releases'] < 100]
fig = px.histogram(slice, x='Releases', nbins=100, log_y=True, width=600, height=400)
fig.show()
fig.write_image('figures/release-count-low.svg')

