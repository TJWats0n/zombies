import os
from PIL import Image
from PIL.ImageOps import invert
import numpy as np
from skimage.color import rgb2hsv

def import_population_as_array(filename):
    print('import_population()')
    input_filename = os.path.join(os.path.dirname(__file__), filename)

    im = Image.open(input_filename)
    width=im.size[0]
    height=im.size[1]

    grayim = im.convert("L")
    # grayim.show()
    p = np.array(grayim)
    density = p/255.0
    density = np.where(density<0.1, 0, density) #make black spots really black
    population = density*3000 #assumption from paper
    return population, width, height


def import_elevation_as_array(filename):
    print('import_elevation()')
    input_filename = os.path.join(os.path.dirname(__file__), filename)
    im = Image.open(input_filename)
    im = np.array(im)
    hsv_im = rgb2hsv(im)
    hue_im = hsv_im[:, :, 0]
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