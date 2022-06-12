import numpy as np
from PIL import Image
import scipy
from structure_tensor import structure_tensor_2d
# import diplib as dp
# import pywt
import math
import matplotlib.pyplot as plt
import cv2

def alignImages(first_img_arr, second_img_arr):
    # first_img = Image.open(img1_name)
    # second_img = Image.open(img2_name)
    # first_img_arr = np.array(first_img)
    # second_img_arr = np.array(second_img)
    DoG_img1 = DoGOperator(first_img_arr)
    DoG_img2 = DoGOperator(second_img_arr)
    threshold1 = calculateThreshold(first_img_arr)
    threshold2 = calculateThreshold(second_img_arr)
    featurePoints1 = featurePoints(DoG_img1, threshold1)
    featurePoints2 = featurePoints(DoG_img2, threshold2)
    features1 = createFeatures(first_img_arr)
    features2 = createFeatures(second_img_arr)
    matches = matchFeatures(features1, features2)
    # img1 = cv2.imread(img1_name,cv2.IMREAD_GRAYSCALE)
    # img2 = cv2.imread(img2_name,cv2.IMREAD_GRAYSCALE)
    new_img, J = executeMatching(matches, featurePoints1, featurePoints2, first_img_arr, second_img_arr)
    return new_img, J



def DoGOperator(np_arr):
    standard_deviation = np.std(np_arr)
    first_gaussian_filter = scipy.ndimage.gaussian_filter(np_arr,standard_deviation)
    second_gaussian_filter = scipy.ndimage.gaussian_filter(np_arr,1.6*standard_deviation)
    DoG = 1.6*(second_gaussian_filter - first_gaussian_filter)/(standard_deviation*2)
    return DoG

def calculateThreshold(np_arr):
    gx, gy = np.gradient(np_arr)
    avg = np.mean(np_arr)
    standard_deviation = np.std(np_arr)
    M = structure_tensor_2d(np_arr,standard_deviation,avg)
    threshold = np.linalg.det(M) - 0.06*((np.trace(M))**2)
    # threshold = dp.Determinant(M) - 0.06*((dp.Trace(M))**2)
    return threshold


def featurePoints(np_arr, value):
    return np.where(np_arr>value)



def createFeatures(img):
    # img = cv2.imread(img_name,cv2.IMREAD_GRAYSCALE)
    surf = cv2.xfeatures2d.SURF_CREATE()
    __, descriptors = surf.DetectAndCompute(img, None)
    return descriptors

def matchFeatures(descriptors1, descriptors2):
    matcherCPU = cv2.BFMatcher(cv2.NORM_L2)
    matches = matcherCPU.knnMatch(descriptors1, descriptors2, k=2)
    selected_matches = sorted(matches, lambda x: x.distance)
    selected_matches = selected_matches[:, int(len(selected_matches)*0.50)]
    return matches

def executeMatching(matches,pointsA, pointsB,im1, im2):
    points1 = np.zeros((len(matches),2),dtype="float")
    points2 = np.zeros((len(matches),2),dtype="float")

    for (i,j) in enumerate(matches):
        points1[i] = pointsA[j.queryIdx].pt
        points2[i] = pointsB[j.trainIdx].pt

    (J, new_mask) = cv2.findHomography(points1, points2, method = cv2.RANSAC)
    heights, widths, channels = im2.shape
    new_im1 = cv2.warpPerspective(im1, J, (widths, heights))
    return new_im1,J
