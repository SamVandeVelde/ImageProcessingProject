import numpy as np
import rawpy
from PIL import Image
from alignment import *
import cv2
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from combination_algos import *
from noise_equalizing import *
from os import listdir
from os.path import isfile, join
from alignment_madeline import *


def perform_stacking():

    global base_path
    global algorithm_index
    global label_error
    global resolution_scaler
    if label_error:
        label_error.destroy()

    if algorithm_index == 0:
        print('SELECT ALGO')
        label_error = Label(gui, text="ERROR no algorithm selected!", fg="red")
        label_error.grid(column=0, row=5)
        return
    if base_path == '':
        print('SELECT basepath')
        label_error = Label(gui, text="ERROR no base path selected!", fg="red")
        label_error.grid(column=0, row=5)
        return

    image_paths = [f for f in listdir(base_path) if isfile(join(base_path, f))]
    rgb_vec = []
    for path in image_paths:
        raw = rawpy.imread(base_path + '/' + path)
        rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=True)
        print(rgb.shape)
        rgb_vec.append(rgb)

    rgb = rgb_vec[0]
    h = rgb_vec[0].shape[0]
    w = rgb_vec[0].shape[1]
    print(f'w:{w}')
    print(f'h:{h}')
    total_images = len(rgb_vec)
    print(f'total_images:{total_images}')
    # for the alignment we use the grayscale image
    # base_gray = np.dot(rgb_vec[0][..., :3], [0.299, 0.587, 0.114])
    # for i in range(1,total_images):
    #     # M = match(rgb_vec[0], rgb_vec[i])
    #     # rgb = cv2.warpPerspective(rgb_vec[i], M, (w, h))
    #     gray_im = np.dot(rgb_vec[i][...,:3], [0.299, 0.587, 0.114])
    #     rgb = alignImages(base_gray, gray_im)
    #     img = Image.fromarray(rgb)
    #     img.show()
    scaler = int(resolution_scaler.get())
    print(f'resolution_scaler.get(): {scaler}')
    rgb = combination_alogs(rgb_vec, ALGO(algorithm_index), scaler)
    # print(rgb)
    img = Image.fromarray(rgb)
    img.show()

    # raw = rawpy.imread('data/New/IMG_0702.CR2')
    # rgb_im = raw.postprocess(use_camera_wb=True, no_auto_bright=True)#no_auto_scale=True)#, no_auto_bright=True)
    # print(rgb_im)
    # print(rgb_im.shape)
    # img = Image.fromarray(rgb_im)
    # img.show()
    # equal_im = noise_equal(rgb_im)
    #
    # print(equal_im)
    # print(rgb_im.shape)
    # print(equal_im.shape)
    # img2 = Image.fromarray(equal_im)
    # img2.show()



def directory():
    # get a directory path by user
    global base_path
    global label_path
    filepath = filedialog.askdirectory(initialdir=r"C:\python\pythonProject", title="Dialog box")
    print(f'filepath: {filepath}')
    if filepath != ():
        base_path = filepath
        if label_path:
            label_path.destroy()
        label_path = Label(gui, text="Selected directory: " + filepath)
        label_path.grid(column=0, row=4, columnspan = 2)


# Function to get the index of selected option in Combobox
def callback_algo(*args):
    global algorithm_index
    algorithm_index = cb.current() + 1
    print(f'algorithm_index:{algorithm_index}')

if __name__ == '__main__':

    gui = Tk()
    gui.title('The image stacker 9001')
    gui.geometry('800x200')
    base_path = ''  # empty string to init
    label_path = None
    label_error = None
    algorithm_index = 0  # 0 to init
    resolution_scaler = IntVar()
    dir_button = Button(gui, text='select image directory', command=directory)
    dir_button.grid(column=0, row=3)

    # Define Options Tuple
    options = ('No rejection', 'Median', 'MINMAX', 'Sigma Clipping', 'Average Sigma Clipping', 'No weight, no rejection', 'Turkey\'s Biweight')
    var = StringVar()
    var.set('Select stacking algorithm of choice')
    cb = ttk.Combobox(gui, textvariable=var)
    cb['values'] = options
    cb.grid(column=0, row=0)

    # Set the tracing for the given variable
    var.trace('w', callback_algo)


    options2 = (1,2,4,8,16,32)

    

    label_res = Label(gui, text="Axial resolution devisor (default=1 i.e. no scaling, 2 --> 1/4 = 1/(2*2) as many pixels)")
    label_res.grid(column=0, row=1, columnspan = 2)

    resolution_scaler = ttk.Combobox(gui, values = options2)

    resolution_scaler.current(0)
    resolution_scaler.grid(column=0, row=2)

    
    start_button = Button(gui, text='start stacking', command=perform_stacking)
    start_button.grid(column=1, row=3)

    gui.mainloop()
