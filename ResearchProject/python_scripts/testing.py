import numpy as np
import cv2
import os
import math
def enlarge(view):
    dir = view + '/TestImages'
    files = os.listdir(dir)

    for file_name in files:
        print(dir + '/' + file_name)
        img = cv2.imread(view + '/TestImages/' + file_name, cv2.IMREAD_UNCHANGED)

        print('Original Dimensions : ',img.shape)

        scale_percent = 300 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite(view + '/TestImages/' + file_name, resized)

def contours(img, low, high):
    red_image = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    red_image[:] = (0, 0, 255)
    lower_gray = np.array([low])
    upper_gray = np.array([high])
    lesion_mask = cv2.inRange(img, lower_gray, upper_gray)
    hull_res = cv2.bitwise_and(red_image, red_image, mask=lesion_mask)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 30))
    gray = cv2.cvtColor(hull_res, cv2.COLOR_BGR2GRAY)
    threshed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, rect_kernel)
    hull_contours, hierarchy = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(hull_res, hull_contours, -1, (0, 255, 0), 1)


    return hull_res 

def get_threshold_vals(img):
    """Creates OpenCV window with selected image. Uses corresponding callback function to show values to user."""
    cv2.namedWindow('image')
    param = [img]
    cv2.setMouseCallback('image', threshold_vals_callback, param)
    while 1:
        cv2.imshow('image', img)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


def threshold_vals_callback(event, x, y, flags, param):
    """Gets values for parameters through listening for mouse clicks on image window"""
    img = param[0]

    # checks event for single click of right mouse button, printing the grayscale value at the point of the click
    if event == cv2.EVENT_LBUTTONDBLCLK:
        val = img[y, x]
        print("Value: ", val)
        print(y,x)

def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))

def central_contour(contours, img_center):
    index = 0
    curr_min = 10000000
    for i in range(len(contours)):
        M = cv2.moments(contours[i])
        if M['m00'] != 0:
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])
            center = (x, y)
            dist = distance(center, img_center)
            if dist < curr_min:
                index = i
                curr_min = dist

    return contours[index]
def draw_contours(poi):
    """Function that draws contour lines on images based on given parameters"""

    print("\nStarting contour drawings!")
    hull_list = []
 
    # Create range to see which images will be processed
    count = 0

    # For loop to go through directory of processed images and apply contour drawing algorithm
    files = os.listdir('./Thresholded')

    for file_name in files:
        file_path = './Thresholded/' + file_name
        res = cv2.imread(file_path)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        # Defines center
        img_center = (poi[0], poi[1])

        # Finds and draws the contours on red background
        edged = cv2.Canny(gray, 100, 200)
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        center_contour = [central_contour(contours, img_center)]
        cv2.drawContours(res, center_contour, -1, (0, 255, 0), 1)

        # Creates convex image

        # Draws contours on isolated spinal cord with MRI background

        # Draws Hull Convexes on both red bg image and MRI background
        hull_res = cv2.imread(file_path)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 30))
        threshed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, rect_kernel)
        hull_contours, hierarchy = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        hull_center_contour = cv2.convexHull(central_contour(hull_contours, img_center))
        hull_list.append(hull_center_contour)
        hull_center_contour = [hull_center_contour]

        thickness = 1

        # if count == 0 or count == len(files) - 1:
        #     thickness = -1

        cv2.drawContours(hull_res, hull_center_contour, -1, (0, 255, 0), thickness)
        
        # Write images into respective directories
        
        count += 1

    # Contour drawing is finished, ask user to retrace any contours
    print('\nFinished contour drawings!\n')
    cv2.imwrite("new.png", hull_res[11])
    return hull_list[11]

if __name__ == '__main__':
    print(draw_contours((96,141)))