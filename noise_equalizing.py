import numpy as np
import rawpy
from PIL import Image


def noise_equal(rgb):
    # each picture is histogram stretched
    print(rgb.shape)
    x_max = rgb.max()
    x_min = rgb.min()
    print(x_min)
    print(x_max)
    temp = np.round(255*((rgb - x_min)/(x_max - x_min)))
    ret = temp.astype('uint8')
    return ret

