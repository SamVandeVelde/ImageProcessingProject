from enum import IntEnum
import multiprocessing as mp
from multiprocessing import Pool
import math
import numpy as np

from noise_equalizing import *


class ALGO(IntEnum):
    NO_REJECTION = 1,
    MEDIAN = 2,
    MINMAX = 3,
    SIGMA_CLIPPING = 4,
    AVG_SIGMA_CLIPPING = 5,
    NO_WEIGHTING_NO_REJECT = 6,
    TURKEYS_BIWEIGHT = 7


def avg(rgb_vec, start_x, stop_x, y_len):
    x_len = stop_x - start_x
    i_len = len(rgb_vec)
    ret = np.zeros([x_len, y_len, 3])
    for x in range(start_x, stop_x):
        if start_x == 0:
            print(f'x: {x}/{stop_x}')
        for y in range(y_len):
            avg = np.zeros([3])
            for index in range(i_len):
                avg += rgb_vec[index][x][y]
            avg = avg / i_len
            ret[x - start_x, y, :] = avg
    return ret


def median(rgb_vec, start_x, stop_x, y_len):
    rbg_stack = np.stack(rgb_vec, axis=0)
    print(f'aaaaaaaaaa {rbg_stack.shape}, {rbg_stack[:,start_x:stop_x,1:y_len,:].shape}')
    return np.round(np.median(rbg_stack[:,start_x:stop_x,1:y_len,:], 0))


def min_max(rgb_vec, start_x, stop_x, y_len):
    x_len = stop_x - start_x
    i_len = len(rgb_vec)
    ret = np.zeros([x_len, y_len, 3], dtype=np.uint8)
    for x in range(start_x, stop_x):
        if start_x == 0:
            print(f'x: {x}/{stop_x}')
        for y in range(y_len):
            values = np.zeros([i_len, 3])
            for index in range(i_len):
                values[index, :] = rgb_vec[index][x][y]

            mask = np.logical_or(values == values.max(1, keepdims=1), values == values.min(1, keepdims=1))
            values_masked = np.ma.masked_array(values, mask=mask)
            avg = np.mean(values_masked, axis=0)
            ret[x - start_x, y, :] = avg
    return ret


def median_var(x):
    med = np.median(x)
    return [np.mean((x - med) ** 2), med]
    # return [np.var(x), med]


def sig_clipping(rgb_vec, start_x, stop_x, y_len):
    x_len = stop_x - start_x
    i_len = len(rgb_vec)
    ret = np.zeros([x_len, y_len, 3], dtype=np.uint8)
    for x in range(start_x, stop_x):
        if start_x == 0:
            print(f'x: {x}/{stop_x}')
        for y in range(y_len):
            values = np.zeros([i_len, 3])
            for index in range(i_len):
                values[index, :] = rgb_vec[index][x][y]

            alpha = 0.67  # WHERE DO I COME FROM # 0.67 => keep 50% of the pixels
            # WERE DO I GO?
            # COTTON EYE JOE??!!

            sigma, med = median_var(values)
            max_keep = med + alpha * sigma
            min_keep = med - alpha * sigma
            mask = np.logical_or(values > max_keep, values < min_keep)
            values_masked = np.ma.masked_array(values, mask=mask)
            avg = np.mean(values_masked, axis=0)
            ret[x - start_x, y, :] = avg
    return ret


def avg_sig_clipping(rgb_vec, start_x, stop_x, y_len):
    x_len = stop_x - start_x
    i_len = len(rgb_vec)
    ret = np.zeros([x_len, y_len, 3], dtype=np.uint8)
    for x in range(start_x, stop_x):
        if start_x == 0:
            print(f'x: {x}/{stop_x}')
        for y in range(y_len):
            values = np.zeros([i_len, 3])
            for index in range(i_len):
                values[index, :] = rgb_vec[index][x][y]

            alpha = 0.67  # WHERE DO I COME FROM # 0.67 => keep 50% of the pixels
            # WERE DO I GO?
            # COTTON EYE JOE??!!

            sigma = np.var(values)
            avg = np.mean(values)
            max_keep = avg + alpha * sigma
            min_keep = avg - alpha * sigma
            mask = np.logical_or(values > max_keep, values < min_keep)

            values_masked = np.ma.masked_array(values, mask=mask)
            avg = np.mean(values_masked, axis=0)
            ret[x - start_x, y, :] = avg
    return ret


def tukeys_biweight(rgb_vec, start_x, stop_x, y_len):
    x_len = stop_x - start_x
    i_len = len(rgb_vec)
    ret = np.zeros([x_len, y_len, 3], dtype=np.int16)
    for x in range(start_x, stop_x):
        if start_x == 0:
            print(f'x: {x}/{stop_x}')
        for y in range(y_len):
            values = np.zeros([i_len, 3])
            for index in range(i_len):
                values[index, :] = rgb_vec[index][x][y]
            sigma = np.var(values)
            med = np.median(values)
            # print(f'med: {med}')
            c = 5 * sigma
            avg = np.zeros([3])
            for index in range(i_len):
                temp_value = rgb_vec[index][x][y]
                # print(f'temp value: {temp_value}')
                weighted_value = np.zeros([3])
                for i in range(len(temp_value)):
                    weighted_value[i] = tukey_function(temp_value[i], c, med)
                avg += weighted_value
            avg = avg / i_len
            ret[x - start_x, y, :] = avg
    return ret


def tukey_function(x, c, med):
    if abs(x - med) > c:
        return 0
    else:
        return med + (x - med) * pow(1 - pow((x - med) / c, 2), 2)


def combination_alogs(rgb_vec, algo, divisor):
    match algo:
        case ALGO.NO_REJECTION:
            # aron
            x_len = len(rgb_vec[0])  // divisor
            print(x_len)
            y_len = len(rgb_vec[0][0])  // divisor
            print(y_len)
            i_len = len(rgb_vec)
            # print(f'shape pre: {rgb_vec[0].shape}, {rgb_vec[0].dtype}')
            N = 16
            p = Pool(N)
            results = []
            for i in range(N):
                arg = (rgb_vec, x_len // N * i, x_len // N * (i + 1), y_len)
                results.append(p.apply_async(avg, arg))

            ret = np.concatenate([res.get(timeout=1000) for res in results])
            ret = gamma_correction(ret, 1)
            # print(f'shape post: {ret.shape}, {ret.dtype}')
            return ret
        case ALGO.MEDIAN:
            # Sam tried
            # Aron Succes!
            x_len = len(rgb_vec[0]) // divisor
            y_len = len(rgb_vec[0][0]) // divisor
            i_len = len(rgb_vec)
            N = 16
            p = Pool(N)
            results = []
            for i in range(N):
                arg = (rgb_vec, x_len // N * i, x_len // N * (i + 1), y_len)
                results.append(p.apply_async(median, arg))
            ret = np.concatenate([res.get(timeout=1000) for res in results])
            ret = gamma_correction(ret, 1)
            return ret

        case ALGO.MINMAX:
            # aron
            x_len = len(rgb_vec[0])  // divisor
            y_len = len(rgb_vec[0][0])  // divisor
            i_len = len(rgb_vec)
            # print(f'shape pre: {rgb_vec[0].shape}, {rgb_vec[0].dtype}')
            N = 16
            p = Pool(N)
            results = []
            for i in range(N):
                arg = (rgb_vec, x_len // N * i, x_len // N * (i + 1), y_len)
                results.append(p.apply_async(min_max, arg))
            ret = np.concatenate([res.get(timeout=1000) for res in results])
            ret = gamma_correction(ret, 1)
            # print(f'shape post: {ret.shape}, {ret.dtype}')
            return ret
        case ALGO.SIGMA_CLIPPING:
            # Aron
            x_len = len(rgb_vec[0]) // divisor
            y_len = len(rgb_vec[0][0]) // divisor
            i_len = len(rgb_vec)
            # print(f'shape pre: {rgb_vec[0].shape}, {rgb_vec[0].dtype}')
            N = 16
            p = Pool(N)
            results = []
            for i in range(N):
                arg = (rgb_vec, x_len // N * i, x_len // N * (i + 1), y_len)
                results.append(p.apply_async(sig_clipping, arg))
            ret = np.concatenate([res.get(timeout=1000) for res in results])
            ret = gamma_correction(ret, 1)
            # print(f'shape post: {ret.shape}, {ret.dtype}')
            return ret
        case ALGO.AVG_SIGMA_CLIPPING:
            # Aron
            x_len = len(rgb_vec[0]) // divisor
            y_len = len(rgb_vec[0][0]) // divisor
            i_len = len(rgb_vec)
            # print(f'shape pre: {rgb_vec[0].shape}, {rgb_vec[0].dtype}')
            N = 16
            p = Pool(N)
            results = []
            for i in range(N):
                arg = (rgb_vec, x_len // N * i, x_len // N * (i + 1), y_len)
                results.append(p.apply_async(avg_sig_clipping, arg))
            ret = np.concatenate([res.get(timeout=10000) for res in results])
            ret = gamma_correction(ret, 1)
            # print(f'shape post: {ret.shape}, {ret.dtype}')
            return ret
        case ALGO.NO_WEIGHTING_NO_REJECT:
            # Louis
            x_len = len(rgb_vec[0]) // divisor
            print(x_len)
            y_len = len(rgb_vec[0][0]) // divisor
            print(y_len)
            i_len = len(rgb_vec)
            # print(f'shape pre: {rgb_vec[0].shape}, {rgb_vec[0].dtype}')
            N = 16
            p = Pool(N)
            results = []
            for i in range(N):
                arg = (rgb_vec, x_len // N * i, x_len // N * (i + 1), y_len)
                results.append(p.apply_async(avg, arg))

            ret = np.concatenate([res.get(timeout=1000) for res in results])
            ret = gamma_correction(ret, 1)
            return ret
        case ALGO.TURKEYS_BIWEIGHT:
            # SAM
            x_len = len(rgb_vec[0]) // divisor
            y_len = len(rgb_vec[0][0]) // divisor
            i_len = len(rgb_vec)
            # print(f'shape pre: {rgb_vec[0].shape}, {rgb_vec[0].dtype}')
            N = 16
            p = Pool(N)
            results = []
            for i in range(N):
                arg = (rgb_vec, x_len // N * i, x_len // N * (i + 1), y_len)
                results.append(p.apply_async(tukeys_biweight, arg))
            ret = np.concatenate([res.get(timeout=1000) for res in results])
            ret = gamma_correction(ret, 1)
            # print(f'shape post: {ret.shape}, {ret.dtype}')
            return ret
        case _:
            assert False
