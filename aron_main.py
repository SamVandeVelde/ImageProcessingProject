import rawpy
from matplotlib import pyplot as plt
from PIL import Image


from combination_algos import *



def aron_main():
    #path = './data/Darks/Darks1.NEF'
    
    base   = './data/Lights/Lights'
    length = 3
    paths  = [f'{base}{i}.NEF' for i in range(1,length+1)]
    
    rgb_vec = []
    for path in paths:
        print(path)
        raw    =  rawpy.imread(path)
        rgb_vec.append(raw.postprocess())

    rgb = combination_alogs(rgb_vec, ALGO.NO_REJECTION)

    img    = Image.fromarray(rgb)
    plt.imshow(img)
    plt.show()

aron_main()

