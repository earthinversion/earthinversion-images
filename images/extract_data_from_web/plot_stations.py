import numpy as np
import pygmt
import pandas as pd
np.random.seed(45)  # to get the same color at each run

df = pd.read_csv('station_list.txt')
print(df.head())

# get the list of networks
networks = list(set(df['Network'].tolist()))

dfs = []
for net in networks:
    df1 = df[df['Network'] == net]
    dfs.append(df1)

colorsList = []
for i in range(len(networks)):
    colorsList.append('#%06X' % np.random.randint(0, 0xFFFFFF))


minlon, maxlon = df['Long.'].min()-1, df['Long.'].max()+1
minlat, maxlat = df['Lat.'].min()-1, df['Lat.'].max()+1

# define etopo data file

topo_data = "@earth_relief_15s"

# Visualization
fig = pygmt.Figure()
# make color pallets
pygmt.makecpt(
    cmap='etopo1',
    series='-8000/5000/1000',
    continuous=True
)

# plot high res topography
fig.grdimage(
    grid=topo_data,
    region=[minlon, maxlon, minlat, maxlat],
    projection='M4i',
    shading=True,
    frame=True
)

# plot coastlines
fig.coast(
    region=[minlon, maxlon, minlat, maxlat],
    projection='M4i',
    shorelines=True,
    frame=True
)
leftjustify, rightoffset = "TL", "5p/-5p"
for idx, dff in enumerate(dfs):
    fig.plot(
        x=dff["Long."].values,
        y=dff["Lat."].values,
        style="i10p",
        color=colorsList[idx],
        pen="black",
        label=networks[idx]
    )

for snum in range(df.shape[0]):
    fig.text(
        x=df.loc[snum, 'Long.'],
        y=df.loc[snum, 'Lat.'],
        text=f"{df.loc[snum, 'Station']}",
        justify=leftjustify,
        angle=0,
        offset=rightoffset,
        fill="white",
        font=f"6p,Helvetica-Bold,black",
    )


fig.legend(position="JTR+jTR+o0.2c", box=True)

fig.savefig('station_map.png', crop=True, dpi=300)
