import os
from PIL import Image
from PIL.ImageOps import invert
import numpy as np
from skimage.color import rgb2hsv
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from math import radians, degrees
from tqdm import tqdm
import itertools
import pickle

def import_population_as_array(filename):
    print('import_population()')
    input_filename = os.path.join(os.path.dirname(__file__), filename)

    im = Image.open(input_filename)



    grayim = im.rotate(-2)
    # grayim.show()
    p = np.array(grayim)

    mask = np.all(p == (0, 255, 0), axis=-1)
    z = np.transpose(np.where(mask))
    print("Coordinates (x,y) of Ryze pixel: (%d,%d)" % (z[0][1], z[0][0]))
    mask = np.all(p == (255, 0, 0), axis=-1)
    z = np.transpose(np.where(mask))
    print("Coordinates (x,y) of Brest pixel: (%d,%d)" % (z[0][1],z[0][0]))

    p = p[:-540, :]  # empirical values to roughly scale both pictures to same size
    p = p[:,:,2] #just choose last layer of grayim -> brest and ryze population must be initialised manually

    width = p.shape[1]
    height = p.shape[0]

    density = p/255.0
    density = np.where(density<0.1, 0, density) #make black spots really black
    population = density*3000 #assumption from paper

    # print('projection')
    # lats, lons = [], []
    # x_orig, y_orig = range(width), range(height)
    #
    # points = list(itertools.product(x_orig,y_orig))
    # for point in tqdm(points):
    #     lats.append(np.interp(point[1], [0,height] , [33.345762, 61.169215]))
    #     lons.append(np.interp(point[0], [0,width], [-11.244216, 45.810121]))
    #
    # with open('lats.pickle', 'wb') as outfile:
    #     pickle.dump(lats, outfile)
    #
    # with open('lons.pickle', 'wb') as outfile:
    #     pickle.dump(lons, outfile)

    # with open('lats.pickle', 'rb') as infile:
    #     lats = pickle.load(infile)
    #
    # with open('lons.pickle', 'rb') as infile:
    #     lons = pickle.load(infile)
    #
    #
    # df1 = pd.DataFrame({'p_ori': points, 'lats': lats, 'lons': lons})

    #p_ori (col, row) -> population[row, col]
    # df1['h_population'] = df1['p_ori'].apply(lambda x: population[height-1-x[1], x[0]])
    # df1['coords'] = list(zip(df1['lats'], df1['lons']))
    # df1['coords'] = df1['coords'].apply(Point)
    # gdf1 = gpd.GeoDataFrame(df1, geometry='coords')

    # with open('gdf.pickle', 'wb') as outfile:
    #     pickle.dump(gdf1, outfile)

    # with open('gdf.pickle', 'rb') as infile:
    #     gdf1 = pickle.load(infile)
    #
    # gdf1.crs = {"init": "epsg:3785"}
    # gdf1 = gdf1.to_crs(epsg=2154)
    #
    # with open('gdf_2154.pickle', 'wb') as outfile:
    #     pickle.dump(gdf1, outfile)
    #
    #
    # lat_deg = 110.574 #one degree of latitude is 110.574km
    # lat_step = 1/lat_deg*15
    #
    # def get_lon_step(latitude):
    #     lon_deg = 111.320*(degrees(np.cos(radians(latitude))))
    #     lon_step = 1/lon_deg*15
    #     return lon_step

    # for node in G.nodes:
    #     x = node[0]
    #     y = node[1]
    #
    #     lon_min, lon_max = -11.244216, 45.810121
    #     lat_min, lat_max = 33.345762, 61.169215
    #
    #     filtered = df1.filter(lon >= lon_min + x*lon_step,  lon < lon_min + (x+1) * lon_step, lat >= lat_min + x*lat_step, lat < lat_min + (x+1) * lat_step )
    #
    #     G.nodes[node]['population'] = filtered['h_population'].sum()

    # ul:
    # lon: -11.244216
    # lat: 61.169215
    #
    # lr:
    # lon: 45.810121
    # lat: 33.345762

    return population, width, height


def import_elevation_as_array(filename):
    print('import_elevation()')
    input_filename = os.path.join(os.path.dirname(__file__), filename)
    im = Image.open(input_filename)
    im = np.array(im)
    hsv_im = rgb2hsv(im)
    hue_im = hsv_im[:, :, 0]
    hue_im = hue_im[1200:-81, : -71] #empirical values to rouhgly scale both pictures to same size
    hue_im = np.where(((hue_im<0.54498) & (hue_im>0.54496)), -1, hue_im) #water hue = 0.54497, np.where() needs this trick

    min = np.min(hue_im)
    max = np.max(hue_im)
    hp_point = 3409 #from requirements/Mont Blanc
    lw_point = 0
    norm_hue_im = np.where(hue_im>=0, lw_point + ((hue_im-min)*(hp_point-lw_point) / (max - min)), hue_im)

    # from matplotlib import pyplot as plt
    # plt.imshow(norm_hue_im)
    # plt.show()

    return norm_hue_im



#import_elevation_as_array('elevation1x1_new-mer-bleue.bmp')