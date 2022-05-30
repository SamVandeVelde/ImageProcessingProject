
from noise_equalizing import *

if __name__ == '__main__':
    raw = rawpy.imread('data/Lights/Lights15.NEF')
    rgb_im = raw.postprocess(use_camera_wb=True, output_bps = 16)  # , no_auto_scale=True, no_auto_bright=True)
    print(rgb_im)
    print(rgb_im.shape)
    img = Image.fromarray(rgb_im, mode='I;16')
    img.show()
    # equal_im = noise_equal(rgb_im)
    #
    # print(equal_im)
    # print(rgb_im.shape)
    # print(equal_im.shape)
    # img2 = Image.fromarray(equal_im)
    # img2.show()
