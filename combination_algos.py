from enum import Enum
import multiprocessing as mp
from multiprocessing import Pool
import math

import numpy as np



class ALGO(Enum):
    NO_REJECTION = 1,
    MEDIAN = 2,
    MINMAX = 3,
    SIGMA_CLIPPING = 4,
    AVG_SIGMA_CLIPPING = 5,
    NO_WEIGHTING_NO_REJECT = 6,
    TURKEYS_BIWEIGHT = 7

def f(rgb_vec, start_x, stop_x):

    y_len = len(rgb_vec[0][0])
    x_len = stop_x - start_x
    i_len = len(rgb_vec)
    ret = np.zeros([x_len, y_len,3], dtype=np.uint8)
    for x in range(start_x, stop_x):
        for y in range(y_len):
            avg = np.zeros([3])
            for index in range(i_len):
                avg += rgb_vec[index][x][y]
            avg = avg/i_len
            ret[x-start_x,y,:] = avg
    return ret

def g(rgb_vec, start_y, stop_y, ret):
    return start_y*stop_y

def combination_alogs(rgb_vec, algo):
    match algo:
        case ALGO.NO_REJECTION:
            # aron
            x_len = len(rgb_vec[0])
            y_len = len(rgb_vec[0][0])
            i_len = len(rgb_vec)
            #print(f'shape pre: {rgb_vec[0].shape}, {rgb_vec[0].dtype}')
            N = 16
            p = Pool(N)
            results = []
            for i in range(N):
                arg = (rgb_vec, x_len//N*i, x_len//N*(i+1))
                results.append(p.apply_async(f, arg))
            ret = np.concatenate([res.get(timeout=100) for res in results])

            #print(f'shape post: {ret.shape}, {ret.dtype}')
            return ret
        case ALGO.MEDIAN:
            # Sam
            x_len = len(rgb_vec[0])
            y_len = len(rgb_vec[0][0])
            i_len = len(rgb_vec)
            ret = np.zeros([x_len, y_len, 3], dtype=np.uint8)
            print(f'shape pre: {rgb_vec[0].shape}, {rgb_vec[0].dtype}')
            for x in range(x_len):
                for y in range(y_len):
                    r_values = []
                    g_values = []
                    b_values = []
                    for index in range(i_len):
                        pixel = rgb_vec[index][x][y]
                        r_values.append(pixel[0])
                        g_values.append(pixel[1])
                        b_values.append(pixel[2])
                    median_result = np.zeros([3])
                    median_result[0] = np.median(r_values)
                    median_result[1] = np.median(g_values)
                    median_result[2] = np.median(b_values)
                    ret[x, y, :] = median_result.astype('d')
            print(f'shape post: {ret.shape}, {ret.dtype}')
            return ret
        case ALGO.MINMAX:
            # aron
            return None
        case ALGO.SIGMA_CLIPPING:
            # Louis
            return None
        case ALGO.AVG_SIGMA_CLIPPING:
            # aron
            return None
        case ALGO.NO_WEIGHTING_NO_REJECT:
            # Louis
            return None
        case ALGO.TURKEYS_BIWEIGHT:
            # aron
            return None
        case _:
            assert False