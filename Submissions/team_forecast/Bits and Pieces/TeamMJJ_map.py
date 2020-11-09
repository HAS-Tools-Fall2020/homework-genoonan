# Team MJJ Location Map

# %%
import os
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import contextily as ctx

# %%
# Dataset 1: USGS stream gauges
# Download Gauges II USGS stream gauge dataset here:
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder

# Read in using geopandas
file = os.path.join('data', 'gagesII_9322_point_shapefile',
                    'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(file)

# Filter to only AZ gauges
gages_AZ = gages[gages['STATE'] == 'AZ']

# %%
# Dataset 2: Watershed boundaries for the Lower Colorado
# Download WBD_15_HU2_GDB.gdb from USGS here:
# https://www.usgs.gov/core-science-systems/ngp/national-hydrography/access-national-hydrography-products
# https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View

# Read in using geopandas
file = os.path.join('data', 'WBD_15_HU2_Shape', 'Shape', 'WBDHU6.shp')
HUC6 = gpd.read_file(file, layer="WBDHU6")

# Filter to only Verde River Watershed
HUC6.columns
HUC6.name.unique()
HUC6_Verde = HUC6[HUC6['name'] == 'Verde']

# %%
# Dataset 3: Major rivers/streams
# Download USA Rivers and Streams from Esri here:
# https://hub.arcgis.com/datasets/esri::usa-rivers-and-streams?geometry=-115.952%2C31.858%2C-109.014%2C33.476

# Read in using geopandas
file = os.path.join('data', 'USA_Rivers_and_Streams-shp',
                    'USA_Rivers_and_Streams.shp')
rivers_USA = gpd.read_file(file)

# Filter to only AZ
rivers_AZ = rivers_USA[rivers_USA['State'] == 'AZ']

# Filter to only Verde
river_Verde = rivers_AZ[rivers_AZ['Name'] == 'Verde River']

# %%
# Dataset 4: Add point location of our stream gage
# https://waterdata.usgs.gov/nwis/inventory/?site_no=09506000&agency_cd=USGS
# Stream gauge:  34.44833333, -111.7891667
point_list = np.array([[-111.7891667, 34.44833333]])

# Make point into spatial feature
point_geom = [Point(xy) for xy in point_list]
point_geom

# Make a dataframe of the point
point_df = gpd.GeoDataFrame(point_geom, columns=['geometry'],
                            crs=HUC6.crs)

# %%
# Re-project datasets to match gages_AZ

points_project = point_df.to_crs(gages_AZ.crs)
HUC6_project = HUC6.to_crs(gages_AZ.crs)
HUC6_Verde_project = HUC6_Verde.to_crs(gages_AZ.crs)
rivers_AZ_project = rivers_AZ.to_crs(gages_AZ.crs)
river_Verde_project = river_Verde.to_crs(gages_AZ.crs)

# %%
# Plot projected datasets together
fig, ax = plt.subplots(figsize=(5, 5))

# Set map extent to zoom in on Verde River watershed
xlim = ([-1600000, -1300000])
ylim = ([1250000, 1600000])
ax.set_xlim(xlim)
ax.set_ylim(ylim)

# Draw layers in specified order using zorder
HUC6_project.boundary.plot(ax=ax, color=None, edgecolor='black', zorder=1,
                           label='Watersheds (HUC2)', linewidth=0.75)
HUC6_Verde_project.boundary.plot(ax=ax, color=None, edgecolor='black',
                                 linewidth=2, zorder=2)
rivers_AZ_project.plot(ax=ax, linewidth=0.5, color='b',
                       label='Rivers/Streams', zorder=3)
river_Verde_project.plot(ax=ax, linewidth=2, color='b', zorder=4)
gages_AZ.plot(ax=ax, markersize=40, marker='^', color='limegreen',
              edgecolor='black', label='USGS stream gage', zorder=5)
points_project.plot(ax=ax, color='yellow', marker='^', edgecolor='black',
                    markersize=70, label='Verde River forecast gage', zorder=6)

# Set map title and axes names
ax.set_title('Verde River Watershed')
ax.set_xlabel('Easting (m)')
ax.set_ylabel('Northing (m)')
ax.legend(loc='upper right', fontsize=7)

# Add Topo basemap and reproject basemap to match gages_AZ
ctx.add_basemap(ax, crs=gages_AZ.crs, url=ctx.providers.OpenTopoMap)
plt.show()

# %%
