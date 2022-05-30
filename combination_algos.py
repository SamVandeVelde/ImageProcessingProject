from enum import enum

class ALGO(enum):
    NO_REJECTION,
    MEDIAN,
    MINMAX,
    SIGMA_CLIPPING,
    AVG_SIGMA_CLIPPING,
    NO_WEIGHTING_NO_REJECT,
    TURKEYS_BIWEIGHT

def combination_alogs(rgb, algo):
    match algos:
        case NO_REJECTION,:
            pass
        case MEDIAN:
            pass
        case MINMAX:
            pass
        case SIGMA_CLIPPING:
            pass
        case AVG_SIGMA_CLIPPING:
            pass
        case NO_WEIGHTING_NO_REJECT:
            pass
        case TURKEYS_BIWEIGHT:
            pass
        case _
            assert False