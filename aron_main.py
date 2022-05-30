

def aron_main():
    path = 'image.nef'
    with rawpy.imread(path) as raw:
        rgb = raw.postprocess()


aron_main()