from mayavi.mlab import *
from collections import deque
import math
import cv2
import os
import numpy as np
from hexagons import Hexagons
from ctypes.wintypes import PSIZE


def central_contour(contours, img_center):
    index = 0
    curr_min = 10000000
    for i in range(len(contours)):
        M = cv2.moments(contours[i])
        if M['m00'] != 0:
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])
            center = (x, y)
            distance = lambda p1, p2 : math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))
            dist = distance(center, img_center)
            if dist < curr_min:
                index = i
                curr_min = dist
    return contours[index]
  
  
def process_images(dir):
    files = os.listdir(dir)
    for file in files:
        file_path = os.path.join(dir, file)
        img = cv2.imread(file_path, 0)
        filtered = cv2.bilateralFilter(img,9,75,75)
        hist = cv2.equalizeHist(filtered)
        smooth = cv2.fastNlMeansDenoising(hist, 70,70,7,21)
        kernel = np.ones((5,5), np.uint8)
        img_dilation = cv2.dilate(smooth, kernel, iterations=1)
        cv2.imwrite(file_path, img_dilation)
    return


def threshold(view, img_range, lower_value, upper_value):
    start = img_range[0]
    end = img_range[1]
    count = 0

    # For loop to go through directory of processed images and apply contour drawing algorithm
    files = os.listdir(view + '/PreProImages')

    for file_name in files:
        # Not in range
        if start > count or end < count:
            count +=1
            continue

        file_path = view + '/PreProImages/' + file_name
        img_gray = cv2.imread(file_path, 0)

        # Creates solid red image with the same dimensions as the current image
        red_image = np.zeros((img_gray.shape[0], img_gray.shape[1], 3), np.uint8)
        red_image[:] = (0, 0, 255)
        lower_gray = np.array([lower_value])
        upper_gray = np.array([upper_value])

        # Creates mask on red image with lesion that was identified with lower and upper vals
        lesion_mask = cv2.inRange(img_gray, lower_gray, upper_gray)
        res = cv2.bitwise_and(red_image, red_image, mask=lesion_mask)
        cv2.imwrite(view + '/Thresholded/' + file_name, res)
        count +=1


def draw_contours(view, img_range, poi):
    """Function that draws contour lines on images based on given parameters"""

    print("\nStarting contour drawings!")
    hull_list = []

    # For loop to go through directory of processed images and apply contour drawing algorithm
    files = os.listdir(view + '/Thresholded')

    for file_name in files:
        file_path = view + '/Thresholded/' + file_name
        original_path = file_path.replace("Thresholded", "PreProImages")
        res = cv2.imread(file_path)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        # Defines center
        img_center = (poi[0], poi[1])

        # Finds and draws the contours on red background 
        #edged = cv2.Canny(gray, 100, 200)
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        center_contour = [central_contour(contours, img_center)]
        cv2.drawContours(res, center_contour, -1, (0, 255, 0), 1)

        # Creates convex image
        img_original = cv2.imread(original_path)
        img_original_convex = cv2.imread(original_path)

        # Draws contours on isolated spinal cord with MRI background
        cv2.drawContours(img_original, contours, -1, (0, 255, 0), 1)

        # Draws Hull Convexes on both red bg image and MRI background
        hull_res = cv2.imread(file_path)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 30))
        threshed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, rect_kernel)
        hull_contours, hierarchy = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        hull_center_contour = cv2.convexHull(central_contour(hull_contours, img_center))
        hull_list.append(hull_center_contour)
        hull_center_contour = [hull_center_contour]

        cv2.drawContours(hull_res, hull_center_contour, -1, (0, 255, 0), 1)
        cv2.drawContours(img_original_convex, hull_center_contour, -1, (0, 255, 0), 1)

        # Write images into respective directories
        cv2.imwrite(view + '/Convex/hull' + file_name, hull_res)
        cv2.imwrite(view + '/OverlayedConvexImages/' + file_name, img_original_convex)

    # Contour drawing is finished, ask user to retrace any contours
    print('\nFinished contour drawings!\n')
    return hull_list
    
    
def retrace_callback(event, x, y, flags, param):
    """Callback function to help user draw lines on image."""
    img = param[0]
    points = param[1]
    # checks for event
    if event == cv2.EVENT_LBUTTONDBLCLK:
        # draws line with new endpoint as selected by user
        cv2.circle(img, (x, y), 4, (255, 0, 0), -1)
        points.append([[x, y]])
        i = len(points) - 1
        if i > 0:
            cv2.line(img, tuple(points[i - 1][0]), tuple(points[i][0]), (0, 0, 255), 1)


def draw_points(img):
    """Creates OpenCV Window with selected image. Draws points in "connect the dots" fashion"""
    points = []
    param = [img, points]
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', retrace_callback, param)

    # Display image and run till the escape key is hit
    while 1:
        cv2.imshow('image', img)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()
    return points


def create_mesh(view):
    h = Hexagons(view + '/Convex', 6)

    h.format_key_points()
    h.create_mesh('./' + view)