import rawpy
from matplotlib import pyplot as plt
from PIL import Image

from combination_algos import *


def sam_main():
    # path = './data/Darks/Darks1.NEF'

    base = './data/Lights/Lights'
    length = 2  # 36
    paths = [f'{base}{i}.NEF' for i in range(1, length + 1)]

    rgb_vec = []
    for path in paths:
        print(path)
        raw = rawpy.imread(path)
        rgb_vec.append(raw.postprocess())

    rgb = combination_alogs(rgb_vec, ALGO.MEDIAN)
    print(f'shape: {rgb.shape}')

    img = Image.fromarray(rgb)
    plt.imshow(img)
    plt.show()


sam_main()

