import numpy as np
import rawpy
from PIL import Image


def noise_equal(rgb):
    # picture is histogram stretched
    x_max = rgb.max()
    x_min = rgb.min()
    temp = np.round(255*((rgb - x_min)/(x_max - x_min)))
    ret = temp.astype('uint8')
    return ret

