import rawpy
from matplotlib import pyplot as plt
from PIL import Image


from combination_algos import *



def aron_main():
    #path = './data/Darks/Darks1.NEF'
    
    #base   = './data/Lights/Lights'
    base   = './data/Darks/Darks'
    length = 10
    paths  = [f'{base}{i}.NEF' for i in range(1,length+1)]
    
    rgb_vec = []
    for path in paths:
        print(path)
        raw    =  rawpy.imread(path)
        rgb_vec.append(raw.postprocess(use_camera_wb=True, no_auto_scale=True, no_auto_bright=True))

    rgb = combination_alogs(rgb_vec, ALGO.NO_REJECTION)

    img    = Image.fromarray(rgb)
    plt.imshow(img)
    plt.show()

aron_main()

