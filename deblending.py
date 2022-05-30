import math
import numpy as np


def get_a11():
    outer_sum = 0
    for j in target_subindex:
        for k in target_subindex:
            outer_sum += get_alpha(locations[j], locations[k])
    return outer_sum


def get_a12():
    outer_sum = 0
    for j in target_subindex:
        for k in nontarget_subindex:
            outer_sum += get_alpha(locations[j], locations[k])
    return outer_sum


def get_a21():
    outer_sum = 0
    for j in nontarget_subindex:
        for k in target_subindex:
            outer_sum += get_alpha(locations[j], locations[k])
    return outer_sum


def get_a22():
    outer_sum = 0
    for j in nontarget_subindex:
        for k in nontarget_subindex:
            outer_sum += get_alpha(locations[j], locations[k])
    return outer_sum


def get_alpha(loc1, loc2):
    d = get_distance(loc1, loc2)
    instr_beam_width = 1  # TODO FIND ACTUAL INSTRUMENT BEAM WIDTH
    return math.exp(-d ** 2 / (2 * instr_beam_width ** 2))


def get_distance(loc1, loc2):
    long_sq = (loc1[0] - loc2[0], 2) + pow(loc1[1] - loc2[1], 2)
    return math.sqrt(long_sq)


locations = [[1, 2], [3, 4], [5, 6], [0, 2], [1, 1], [7, 8]]  # TODO GET ACTUAL LOCATIONS
meas_flux = [5, 11, 12, 4, 2, 9]  # TODO GIVE ME THE INTENSITIES!!!
target_positions = [1, 0, 0, 1, 0, 1]
am_known_objects = len(locations)
target_subindex = []
nontarget_subindex = []
for i in range(am_known_objects):
    if target_positions[i] == 1:
        target_subindex.append(i)
    else:
        nontarget_subindex.append(i)

target_locations = []
nontarget_locations = []
target_meas_flux = []
nontarget_meas_flux = []
for i in target_subindex:
    target_locations.append(locations[i])
    target_meas_flux.append(meas_flux[i])
for i in nontarget_subindex:
    nontarget_locations.append(locations[i])
    nontarget_meas_flux.append(meas_flux[i])

# to solve: Ax = b
A = np.zeros((2, 2))
A[0, 0] = get_a11()
A[0, 1] = get_a12()
A[1, 0] = get_a21()
A[1, 1] = get_a22()
B = np.zeros((2, 1))
B[0, 0] = sum(target_meas_flux)
B[1, 0] = sum(nontarget_meas_flux)

x = np.linalg.solve(A,B)
I0 = x[0]
I1 = x[1]
