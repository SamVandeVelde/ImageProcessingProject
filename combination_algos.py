from enum import Enum
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

def combination_alogs(rgb_vec, algo):
    match algo:
        case ALGO.NO_REJECTION:
            # aron
            x_len = len(rgb_vec[0])
            y_len = len(rgb_vec[0][0])
            i_len = len(rgb_vec)
            ret = np.zeros([x_len, y_len,3], dtype=np.uint8)
            print(f'shape pre: {rgb_vec[0].shape}, {rgb_vec[0].dtype}')
            for x in range(x_len):
                for y in range(y_len):
                    avg = np.zeros([3])
                    for index in range(i_len):
                        avg += rgb_vec[index][x][y]
                    avg = avg/i_len
                    ret[x,y,:] = avg.astype('d')
            print(f'shape post: {ret.shape}, {ret.dtype}')
            return ret
        case ALGO.MEDIAN:
            # Louis
            return None
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