import numpy as np
import rawpy
from PIL import Image


def noise_equal(rgb):
    # each picture is histogram stretched
    print(rgb.shape)
    x_len = len(rgb[0])
    y_len = len(rgb)
    # ret = np.zeros([y_len, x_len, 3], dtype=np.uint8)
    # print(ret.shape)
    x_max = rgb.max()
    x_min = rgb.min()
    print(x_min)
    print(x_max)
    # for x in range(x_len):
    #     for y in range(y_len):
    #         ret[y, x] = (rgb[y, x] - x_min) / (x_max - x_min)
    # return ret
    temp = np.round(255*((rgb - x_min)/(x_max - x_min)))
    ret = temp.astype('uint8')
    return ret


def build_raw_array(raw_obj, rows, columns):
    ret = np.zeros([rows, columns, 4], dtype=np.uint8)
    for x in range(rows):
        for y in range(columns):
            color_index = raw_obj.raw_color(x, y)
            ret[x, y, color_index] = raw_obj.raw_value(x, y)
    return ret

if __name__ == '__main__':
    raw = rawpy.imread('data/Lights/Lights15.NEF')
    raw_arr = build_raw_array(raw, 2868, 4320)
    print(raw)
    print(raw_arr)
    print(raw_arr.shape)
    rgb_im = raw.postprocess(use_camera_wb=True, no_auto_scale=True, no_auto_bright=True, four_color_rgb=False)
    # rgb_im = raw.raw_image.copy()
    print(rgb_im)
    equal_im = noise_equal(rgb_im)
    img = Image.fromarray(rgb_im)
    img.show()
    print(equal_im)
    print(rgb_im.shape)
    print(equal_im.shape)
    img2 = Image.fromarray(equal_im)
    img2.show()
