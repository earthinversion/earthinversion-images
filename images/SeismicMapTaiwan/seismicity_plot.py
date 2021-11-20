import pygmt
import pandas as pd
# 1995-07-05 17:33:48.600 24.8313 122.1158 27 4.87
# this file is retrieved from the pygmt dataset
data = pd.read_csv('evtlist.dat', names=['SN','year','time','latitude','longitude','depth_km','magnitude'], delimiter='\s+')


minlon, maxlon = 119.5, 124.0
minlat, maxlat = 19.8, 26.0
# Load sample earth relief data
grid = pygmt.datasets.load_earth_relief(resolution="03s", region=[minlon, maxlon, minlat, maxlat])

maxdep = 10000
frame =  ["xa1f0.25","ya1f0.25", "z2000+lmeters", "wSEnZ"]

pygmt.makecpt(
        cmap='geo',
        series=f'-{maxdep}/4000/100',
        continuous=True
    )
fig = pygmt.Figure()
fig.grdview(
    grid=grid,
    region=[minlon, maxlon, minlat, maxlat, -maxdep, 4000],
    perspective=[150, 30],
    frame=frame,
    projection="M15c",
    zsize="4c",
    surftype="i",
    plane=f"-{maxdep}+gazure",
    shading=0,
    # Set the contour pen thickness to "1p"
    contourpen="1p",
)
# fig.basemap(
#     perspective=True,
#     rose="jTL+w3c+l+o-2c/-1c" #map directional rose at the top left corner 
# )
depthData = data.depth_km.values
depthData = maxdep*(depthData - data.depth_km.min())/(data.depth_km.max()-data.depth_km.min())
# print(depthData)

# colorbar colormap
pygmt.makecpt(cmap="jet", series=[
              depthData.min(), depthData.max()])
# pygmt.makecpt(cmap="jet", series=[
#               data.depth_km.min(), data.depth_km.max()])
fig.plot3d(
    x=data.longitude,
    y=data.latitude,
    z=-1*depthData,
    size=0.05*data.magnitude,
    color=depthData,
    cmap=True,
    style="cc",
    pen="black",
    perspective=True,
)
pygmt.makecpt(cmap="jet", series=[
              data.depth_km.min(), data.depth_km.max()])
fig.colorbar(frame='af+l"Depth (km)"', perspective=True,)

print(data.depth_km.min(), data.depth_km.max())
print(data.magnitude.min(), data.magnitude.max())

# fig.colorbar(perspective=True, frame=["a2000", "x+l'Elevation in (m)'", "y+lm"])
fig.savefig("topo-plot_3d.png", crop=True, dpi=300)


