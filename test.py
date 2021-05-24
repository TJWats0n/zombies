from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np

from skimage import data
from skimage.color import rgb2hsv


# def HSVColor(img):
#     if isinstance(img,Image.Image):
#         r,g,b = img.split()
#         Hdat = []
#         Sdat = []
#         Vdat = []
#         for rd,gn,bl in zip(r.getdata(),g.getdata(),b.getdata()) :
#             h,s,v = colorsys.rgb_to_hsv(rd/255.,gn/255.,bl/255.)
#             Hdat.append(int(h*255.))
#             Sdat.append(int(s*255.))
#             Vdat.append(int(v*255.))
#         r.putdata(Hdat)
#         g.putdata(Sdat)
#         b.putdata(Vdat)
#         return Image.merge('RGB',(r,g,b))
#     else:
#         return None

input_filename = os.path.join(os.path.dirname(__file__), 'elevation1x1_new-mer-bleue.bmp')

pic = Image.open(input_filename)
pic = np.array(pic)
hsv_img = rgb2hsv(pic)
hue_img = hsv_img[:,:,0]
value_img = hsv_img[:,:,2]

fig, (ax0, ax1, ax2) = plt.subplots(ncols=3)
ax0.imshow(hsv_img)
ax0.set_title('HSV')

ax1.imshow(hue_img)
ax1.set_title('HUE')

ax2.imshow(value_img)
ax2.set_title('Value')

plt.show()