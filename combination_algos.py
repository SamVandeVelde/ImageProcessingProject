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
        case ALGO.NO_REJECTION:
            # aron
            return []
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
        case _
            assert False