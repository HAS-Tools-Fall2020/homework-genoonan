# %%
import os
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import fiona
from shapely.geometry import Point
import contextily as ctx

# %%
#  Gauges II USGS stream gauge dataset:
# Download here:
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder

# Reading it using geopandas
file = os.path.join('data', 'gagesII_9322_point_shapefile',
                    'gagesII_9322_sept30_2011.shp')
gages = gpd.read_file(file)

# %%
type(gages)

# %%
gages.head()

# %%
gages.columns

# %%
gages.shape

# %%
# Looking at the geometry now
gages.geom_type

# %%
# check our CRS - coordinate reference system
gages.crs

# %%
# Check the spatial extent
gages.total_bounds

# %%
# Now lets make a map!
fig, ax = plt.subplots(figsize=(5, 5))
gages.plot(ax=ax)
plt.show()

# %%
# Zoom  in and just look at AZ
gages.STATE.unique()

# %%
gages_AZ = gages[gages['STATE'] == 'AZ']
gages_AZ.shape

# %%
# Basic plot of AZ gages
fig, ax = plt.subplots(figsize=(5, 5))
gages_AZ.plot(ax=ax)
plt.show()

# %%
# //////////////
# USGS Watershed Boundary Dataset (WBD) for 2-digit Hydrologic Unit - 15
# (published 20201002)
# download: https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View#productSearch
# Reading it using geopandas
file = os.path.join('data', 'WBD_15_HU2_Shape', 'Shape', 'WBDHU6.shp')
fiona.listlayers(file)

# %%
wshed = gpd.read_file(file)

# %%
type(wshed)

# %%
wshed.head()

# %%
wshed.columns

# %%
wshed.shape

# %%
# Looking at the geometry now
wshed.geom_type

# %%
wshed.crs

# %%
wshed.total_bounds

# %%
fig, ax = plt.subplots(figsize=(5, 5))
wshed.plot(ax=ax)
plt.show()

# %%
# //////////////////////
# USGS National Boundary Dataset
# https://www.sciencebase.gov/catalog/item/59fa9f59e4b0531197affb13

# Reading it using geopandas
file = os.path.join('data', 'GOVTUNIT_Arizona_State_Shape',
                    'Shape', 'GU_StateOrTerritory.shp')
fiona.listlayers(file)

# %%
state = gpd.read_file(file)

# %%
state.crs

# %%
fig, ax = plt.subplots(figsize=(5, 5))
state.plot(ax=ax)
plt.show()

# %%
# Add some points
# Phoenix:  33.448, -112.074
# Tucson: 32.2226, -110.9747
cities_list = np.array([[-112.074, 33.448], [-110.9747, 32.2226]])

# %%
# make these into spatial features
cities_geom = [Point(xy) for xy in cities_list]
cities_geom

# %%
# map a dataframe of these points
cities_df = gpd.GeoDataFrame(cities_geom, columns=['geometry'],
                             crs=state.crs)

# %%
# /////////////////
# Plotting

# Check crs alignment for layers
print("Gages_AZ crs:", gages_AZ.crs, "\n")
print("Watershed crs:", wshed.crs, "\n")
print("State Boundary crs:", state.crs, "\n")
print("Cities crs =", cities_df.crs, "\n")

# %%
# reproject gages
gages_AZ_project = gages_AZ.to_crs(state.crs)

# %%
# Plot all layers
fig, ax = plt.subplots(figsize=(15, 15))
state.boundary.plot(ax=ax, label="State Boundaries", alpha=0.5, color="b")
gages_AZ_project.plot(ax=ax, color='yellow', label="AZ Stream Gauges",
                      markersize=10)
cities_df.plot(ax=ax, color='red', marker='*', label="Major AZ Cities",
               markersize=30)
wshed.boundary.plot(ax=ax, color="black", alpha=0.4, label="HUC6 Watershed")
ctx.add_basemap(ax, url=ctx.providers.OpenTopoMap, crs='epsg:4269')
ax.set_title("Arizona Stream Gauges and HUC6 Watershed Boundary")
ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True,
          ncol=2, framealpha=0.9, facecolor='white', labelcolor='black')
plt.show()

fig.savefig('Noonan_HW10_map.png')

# ///////////////////////////
# WORKS IN PROGRESS

# Add stream gauge point
# Stream gauge lat/long:  34.44833333, -111.7891667
# stream_gauge = [-111.7891667, 34.44833333]


# HydroRIVERS dataset:
# Can't figure out how to filter the rivers I want and data set is SO big (all of North America).
# Download here:
# https://hydrosheds.org/page/hydrorivers
# documentation: https://hydrosheds.org/images/inpages/HydroRIVERS_TechDoc_v10.pdf

# Reading it using geopandas
# file = os.path.join('data', 'HydroRIVERS_v10_na_shp', 'HydroRIVERS_v10_na_shp', 'HydroRIVERS_v10_na.shp')
# rivers = gpd.read_file(file)

# type(rivers)

# rivers.tail()

# rivers.columns

# rivers.shape

# rivers.geom_type

# rivers.crs

# rivers.total_bounds

# fig, ax =plt.subplots(figsize=(5,5))
# rivers.plot(ax=ax)
# plt.show()

# rivers.MAIN_RIV.unique()

# %%
