import rawpy
from PIL import Image
raw = rawpy.imread('data/Lights15.NEF')
print(raw)
rgb = raw.postprocess()
img = Image.fromarray(rgb) # Pillow image
print(img)
img.show() # show on screen