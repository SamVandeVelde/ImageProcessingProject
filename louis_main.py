import imageio
from noise_equalizing import *

if __name__ == '__main__':
    rgb = imageio.imread('data/Lights/darktable_exported/Lights1.jpg')
    # rgb_im = raw.postprocess(use_camera_wb=True, output_bps = 16)  # , no_auto_scale=True, no_auto_bright=True)
    print(rgb)
    print(rgb.shape)
    img = Image.fromarray(rgb)
    img.show()
    equal_im = noise_equal(rgb)
    #
    print(equal_im)
    # print(rgb_im.shape)
    print(equal_im.shape)
    img2 = Image.fromarray(equal_im)
    img2.show()
