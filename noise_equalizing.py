import numpy as np


def gamma_correction(rgb, gamma):
    # each picture is histogram stretched
    print(rgb.shape)
    x_max = rgb.max()
    x_min = rgb.min()
    print(x_min)
    print(x_max)
    temp = np.round(255*np.power(((rgb - x_min)/(x_max - x_min)), gamma))
    ret = temp.astype('uint8')
    return ret

