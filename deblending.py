import math
import numpy as np


def get_a11(instr_beamwidth):
    outer_sum = 0
    for j in target_subindex:
        for k in target_subindex:
            outer_sum += get_alpha(locations[j], locations[k], instr_beamwidth)
    return outer_sum


def get_a12(instr_beamwidth):
    outer_sum = 0
    for j in target_subindex:
        for k in nontarget_subindex:
            outer_sum += get_alpha(locations[j], locations[k], instr_beamwidth)
    return outer_sum


def get_a21(instr_beamwidth):
    outer_sum = 0
    for j in nontarget_subindex:
        for k in target_subindex:
            outer_sum += get_alpha(locations[j], locations[k], instr_beamwidth)
    return outer_sum


def get_a22(instr_beamwidth):
    outer_sum = 0
    for j in nontarget_subindex:
        for k in nontarget_subindex:
            outer_sum += get_alpha(locations[j], locations[k], instr_beamwidth)
    return outer_sum


def get_alpha(loc1, loc2, instr_beamwidth):
    d = get_distance(loc1, loc2)
    return math.exp(-d ** 2 / (2 * instr_beamwidth ** 2))


def get_distance(loc1, loc2):
    long_sq = pow(loc1[0] - loc2[0], 2) + pow(loc1[1] - loc2[1], 2)
    return math.sqrt(long_sq)


def get_target_locations(locations, meas_flux, percentage):
    # returns binarray containing which locations are targets
    # input arguments:
    #   locations: an array containing the [x,y]-coordinate of each target AND non-target position
    #   meas_flux: an array containing the measured fluxes on all these locations.
    #   percentage: the percentage of targets we expect
    threshold_min = np.min(meas_flux)
    threshold_max = np.max(meas_flux)
    temp_threshold = threshold_min
    target_len = percentage * len(locations)
    while temp_threshold != threshold_max:
        target_indices = []
        for i in range(len(locations)):
            if meas_flux[i] > temp_threshold:
                target_indices.append(i)
        if len(target_indices) < target_len:
            target_positions = [0] * len(locations)
            for i in target_indices:
                target_positions[i] = 1
            return target_positions
    raise Exception("There is something wrong with your array; try again")


def deblending(locations, meas_flux, target_positions, instr_beamwidth):
    # returns the actual flux values of the target and non-target positions.
    # input arguments:
    #   locations: an array containing the [x,y]-coordinate of each target AND non-target position
    #   meas_flux: an array containing the measured fluxes on all these locations.
    #   target_positions: an array indicating which locations are target positions and which aren't (binarray)
    #   (Suggestion for finding: the get_targets function above)
    #   instr_beamwidth: the beamwidth of the photographic device used. (if not known, experiment with this value)
    # output arguments: I0, I1 (tuple)
    #   I0: the intrinsic flux values of all target positions (assumed to be constant over all)
    #   I1: the intrinsic flux values of all non-target positions (assumed to be constant over all)
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
    A[0, 0] = get_a11(instr_beamwidth)
    A[0, 1] = get_a12(instr_beamwidth)
    A[1, 0] = get_a21(instr_beamwidth)
    A[1, 1] = get_a22(instr_beamwidth)
    B = np.zeros((2, 1))
    B[0, 0] = sum(target_meas_flux)
    B[1, 0] = sum(nontarget_meas_flux)

    x = np.linalg.solve(A, B)
    I0 = x[0]
    I1 = x[1]
    return I0, I1

# locations = [[1, 2], [3, 4], [5, 6], [0, 2], [1, 1], [7, 8]]  # TODO GET ACTUAL LOCATIONS
# meas_flux = [5, 11, 12, 4, 2, 9]  # TODO GIVE ME THE INTENSITIES!!!
# target_positions = [1, 0, 0, 1, 0, 1]
# am_known_objects = len(locations)
# target_subindex = []
# nontarget_subindex = []
# for i in range(am_known_objects):
#    if target_positions[i] == 1:
#        target_subindex.append(i)
#    else:
#        nontarget_subindex.append(i)

# target_locations = []
# nontarget_locations = []
# target_meas_flux = []
# nontarget_meas_flux = []
# for i in target_subindex:
#    target_locations.append(locations[i])
#    target_meas_flux.append(meas_flux[i])
# for i in nontarget_subindex:
#    nontarget_locations.append(locations[i])
#    nontarget_meas_flux.append(meas_flux[i])

# to solve: Ax = b
# A = np.zeros((2, 2))
# A[0, 0] = get_a11()
# A[0, 1] = get_a12()
# A[1, 0] = get_a21()
# A[1, 1] = get_a22()
# B = np.zeros((2, 1))
# B[0, 0] = sum(target_meas_flux)
# B[1, 0] = sum(nontarget_meas_flux)

# x = np.linalg.solve(A, B)
# I0 = x[0]
# I1 = x[1]
