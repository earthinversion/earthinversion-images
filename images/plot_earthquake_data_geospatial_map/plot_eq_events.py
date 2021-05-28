import pygmt
import pandas as pd
# data = pygmt.datasets.load_japan_quakes()
# data.to_csv('my_events_data.csv', index=False)

# this file is retrieved from the pygmt dataset
data = pd.read_csv('my_events_data.csv')

# Set the region
region = [
    data.longitude.min() - 1,
    data.longitude.max() + 1,
    data.latitude.min() - 1,
    data.latitude.max() + 1,
]


fig = pygmt.Figure()
# fig.basemap(region=region, projection="M15c", frame=True)

# make color pallets
pygmt.makecpt(
    cmap='etopo1',
    series='-8000/5000/1000',
    continuous=True
)

# define etopo data file
topo_data = "@earth_relief_30s"
# plot high res topography
fig.grdimage(
    grid=topo_data,
    region=region,
    projection='M4i',
    shading=True,
    frame=True
)
fig.coast(shorelines=True, frame=True)

# colorbar colormap
pygmt.makecpt(cmap="jet", series=[
              data.depth_km.min(), data.depth_km.max()])
fig.plot(
    x=data.longitude,
    y=data.latitude,
    sizes=0.1*data.magnitude,
    color=data.depth_km,
    cmap=True,
    style="cc",
    pen="black",
)
fig.colorbar(frame='af+l"Depth (km)"')
fig.savefig('my_earthquakes.png')
