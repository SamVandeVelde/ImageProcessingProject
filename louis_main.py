import numpy as np
import rawpy
from PIL import Image
from alignment import *
import cv2

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

    rgb = rgb_vec[0]
    h = rgb_vec[0].shape[0]
    w = rgb_vec[0].shape[1]
    print(w)
    print(h)
    total_images = len(rgb_vec)
    print(total_images)
    for i in range(total_images):
        M = match(rgb_vec[0], rgb_vec[i])
        rgb_vec[i] = cv2.warpPerspective(rgb_vec[i], M, (w, h))

    rgb = combination_alogs(rgb_vec, ALGO.NO_REJECTION)
    #print(rgb)
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
