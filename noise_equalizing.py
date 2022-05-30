import numpy as np
import rawpy
from PIL import Image


def noise_equal(rgb):
    # each picture is histogram stretched
    print(rgb.shape)
    x_len = len(rgb[0])
    y_len = len(rgb)
    ret = np.zeros([y_len, x_len, 3])
    print(ret.shape)
    x_max = rgb.max()
    x_min = rgb.min()
    # for x in range(x_len):
    #     for y in range(y_len):
    #         ret[y, x] = (rgb[y, x] - x_min) / (x_max - x_min)
    # return ret
    ret = np.round((rgb - x_min)/(x_max - x_min))
    return ret


raw = rawpy.imread('data/Darks/Darks1.NEF')
rgb_im = raw.postprocess()
equal_im = noise_equal(rgb_im)
img = Image.fromarray(rgb_im)
img.show()
print(rgb_im.shape)
print(equal_im.shape)
img2 = Image.fromarray(equal_im)
img2.show()
