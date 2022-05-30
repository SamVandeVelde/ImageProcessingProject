import imageio
from matplotlib import pyplot as plt
from PIL import Image


from combination_algos import *



def dark_res():
    #path = './data/Darks/Darks1.NEF'
    
    #base   = './data/Lights/darktable_exported/Lights'
    base   = './data2/Darks/Darks'
    length = 12
    paths  = [f'{base}{i}.jpg' for i in range(1,length+1)]
    
    rgb_vec = []
    for path in paths:
        print(path)
        rgb    =  imageio.imread(path)
        rgb_vec.append(rgb)

    rgb = combination_alogs(rgb_vec, ALGO.NO_REJECTION)

    img    = Image.fromarray(rgb)
    img.show()


def aron_main():
    #path = './data/Darks/Darks1.NEF'
    
    #base   = './data/Lights/darktable_exported/Lights'
    #base   = './data2/Darks/Darks'
    base   = './data2/lights/Lights'
    path_dark   = './data2/DARK_12_FULL_RES.PNG'
    length = 1
    paths  = [f'{base}{i}.jpg' for i in range(1,length+1)]
    
    rgb_vec = []
    for path in paths:
        print(path)
        rgb    =  imageio.imread(path)
        rgb_vec.append(rgb)

    rgb = combination_alogs(rgb_vec, ALGO.NO_REJECTION)

    img    = Image.fromarray(rgb)
    img.show()

    dark   =  imageio.imread(path_dark)
    rgb   = np.abs(rgb - dark[0:2848,0:4316,:])

    img    = Image.fromarray(rgb)
    img.show()
    #plt.imshow(img)
    #plt.show()

aron_main()

