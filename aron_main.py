import rawpy
from matplotlib import pyplot as plt


def aron_main():
    path = './data/Darks/Darks1.NEF'
    with rawpy.imread(path) as raw:
        rgb = raw.postprocess()
        print(rgb)
        plt.imshow(rgb, interpolation='nearest')
        plt.show()


aron_main()