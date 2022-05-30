import imageio
from matplotlib import pyplot as plt
from PIL import Image


from combination_algos import *



def aron_main():
    #path = './data/Darks/Darks1.NEF'
    
    base   = './data/Lights/darktable_exported/Lights'
    #base   = './data/Darks/darktable_exported/Darks'
    length = 1
    paths  = [f'{base}{i}.jpg' for i in range(1,length+1)]
    
    rgb_vec = []
    for path in paths:
        print(path)
        rgb    =  imageio.imread(path)
        rgb_vec.append(rgb)

    #rgb = combination_alogs(rgb_vec, ALGO.NO_REJECTION)

    img    = Image.fromarray(rgb)
    img.show()
    #plt.imshow(img)
    #plt.show()

aron_main()

