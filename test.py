from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np

from skimage import data
from skimage.color import rgb2hsv
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
from skimage.color import rgb2hsv
from createGraph import create_nodes


import matplotlib.pyplot as plt
import networkx as nx
height, width = 6,6
agg_factor = 2
rows, columns = int(height/agg_factor), int(width/agg_factor)
population_img = np.random.randint(0, 10, (rows, columns))

G = create_nodes(rows, columns)

positions = {}
for node in G.nodes:
    positions[node] = [node[0], node[1]]
pos = nx.spring_layout(G, pos=positions, fixed=positions.keys())

plt.figure()
print('drawing')
nx.draw_networkx(G, pos, node_size=5, width=0.1, with_labels=True)
plt.show()


im1 = Image.open("elevation1x1_new-mer-bleue.bmp")
im1 = np.array(im1)
hsv_im = rgb2hsv(im1)
hue_im = hsv_im[:, :, 0]
hue_im = hue_im[1200:-81,: -71]

im2 = Image.open("population-density-map.bmp")
#im2 = im2.rotate(-5)
im2 = np.array(im2)
im2 = im2[:,:,0]

im2 = im2[:-540,:]

plt.figure()
plt.imshow(hue_im)
plt.show()

fig, (ax1, ax2) = plt.subplots(ncols=2)

ax1.imshow(hue_im)
ax2.imshow(im2)

plt.show()
#
# ul:
# x achse: -11.244216 (lon, 2.wert in maps)
# y. 61.169215
#
#
# lr
# lon 45.810121
# lat 33.345762
#
# convert mercartor picture pixel combinations to lat, lon,
# project to lambert sth.
# aggregate based on 15 km (lon, lat), use amount of values of aggregation as how many values in original picture are grouped
# theory, the lower the more values are grouped into on point (differing from the usual 15x15)






# extract the x and y coordinates as flat arrays
arr1x = np.ravel(hue_im[0])
arr1y = np.ravel(hue_im[1])

arr1x = range(0,100)
arr1y = range(0,100)

# using the X and Y columns, build a dataframe, then the geodataframe
df1 = pd.DataFrame({'X':arr1x, 'Y':arr1y})
df1['coords'] = list(zip(df1['X'], df1['Y']))
df1['coords'] = df1['coords'].apply(Point)
gdf1 = gpd.GeoDataFrame(df1, geometry='coords')

gdf1.crs = {"init": "epsg:2154"}
gdf1 = gdf1.to_crs(epsg=3785)

gdf1['y_new'] = gdf1['coords'].y
gdf1['x_new'] = gdf1['coords'].x

min_x = gdf1['x_new'].min()
min_y = gdf1['y_new'].min()

max_x = gdf1['x_new'].max()
max_y = gdf1['y_new'].max()

gdf1.plot()