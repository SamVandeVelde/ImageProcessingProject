import cv2
import numpy as np


# compute a homography (3x3 transform matrix for 2D homogenous coordinates)
# that projects image 1 onto image 2. We use this to line up multiple images
# of the sky that were taken at different times, with the camera at a slightly
# different angle, etc.


def match(im1, im2):
    # OpenCV ORB requires uint8 for some reason

    # Identify interesting points in the image (i.e. stars)
    det = cv2.ORB_create(nfeatures=50000)
    kp1, desc1 = det.detectAndCompute(im1, None)
    kp2, desc2 = det.detectAndCompute(im2, None)
    # Matches up interesting points in both images, based on their descriptors
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc1, desc2)
    # Pick the top 10% of matches (by hamming distance of their descriptor vectors)
    matches = sorted(matches, key=lambda x: x.distance)
    matches = matches[:len(matches) // 10]
    if len(matches) < 10:
        raise Exception("<10 matching descriptors, poor match")
    # Get the coordinates of the matching stars in each image
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    # Calculate a homography matrix from our set of probably-matching stars.
    # The RANSAC algorithm will try to discard inconsistent outliers.
    # Mask tells us which matches seem internally consistent.
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if mask.sum() < 10:
        raise Exception("<10 RANSAC inlier descriptors, poor match")
    return M
