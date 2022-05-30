from enum import Enum
import math

class ALGO(Enum):
    NO_REJECTION,
    MEDIAN,
    MINMAX,
    SIGMA_CLIPPING,
    AVG_SIGMA_CLIPPING,
    NO_WEIGHTING_NO_REJECT,
    TURKEYS_BIWEIGHT

def combination_alogs(rgb_vec, algo):
    match algos:
        case ALGO.NO_REJECTION,:
            return []
        case ALGO.MEDIAN:
            return None
        case ALGO.MINMAX:
            return None
        case ALGO.SIGMA_CLIPPING:
            return None
        case ALGO.AVG_SIGMA_CLIPPING:
            return None
        case ALGO.NO_WEIGHTING_NO_REJECT:
            return None
        case ALGO.TURKEYS_BIWEIGHT:
            return None
        case _
            assert False