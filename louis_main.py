import numpy as np
import rawpy
from PIL import Image

from combination_algos import *
from noise_equalizing import *
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':
    base_path = 'data/New/'
    image_paths = [f for f in listdir(base_path) if isfile(join(base_path, f))]

    rgb_vec = []
    for path in image_paths:
        raw = rawpy.imread(base_path+path)
        rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=True)
        print(rgb.shape)
        rgb_vec.append(rgb)

    rgb = combination_alogs(rgb_vec, ALGO.MINMAX)

    img = Image.fromarray(rgb)
    img.show()

    # raw = rawpy.imread('data/New/IMG_0702.CR2')
    # rgb_im = raw.postprocess(use_camera_wb=True, no_auto_bright=True)#no_auto_scale=True)#, no_auto_bright=True)
    # print(rgb_im)
    # print(rgb_im.shape)
    # img = Image.fromarray(rgb_im)
    # img.show()
    # equal_im = noise_equal(rgb_im)
    #
    # print(equal_im)
    # print(rgb_im.shape)
    # print(equal_im.shape)
    # img2 = Image.fromarray(equal_im)
    # img2.show()
