# Dependencies
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import ui_dependencies as dpnd
import cv2
import numpy as np
import os
import compute
import copy

# Global variables
thresh_vals = []
range_vals = []
poi = []
win = tk.Tk()


def start_callback(view):
    """Callback function for the start button. Asks user to use default or custom parameters."""
    mb.showinfo(title="Select Base Image", message=dpnd.file_msg)
    file_select = tk.Button(text='Click to Open Base Image File',
                            command=lambda:parameter_callback(view)).pack(fill=tk.X)


def parameter_callback(view):
    """Callback function that guides user with selecting parameter values."""
    global thresh_vals, range_vals, poi, win

    win.update()
    # Gets a base image and asks user to trace spinal cord
    base_dir = 'C:/Users/prath/Desktop/ResearchProject/ResearchProject/python_scripts/' + view + "/TestImages"
    file_path = fd.askopenfilename(initialdir=base_dir)
    img = cv2.imread(file_path)
    mb.showinfo(title="Isolate Spinal Cord", message=dpnd.isolate_sc_msg)
    crop_points(view + '/TestImages', view + '/Isolated', img)

    # Shows user isolated spinal cords and asks them to trace around the region of interest
    isolated_dir = 'C:/Users/prath/Desktop/ResearchProject/ResearchProject/python_scripts/' + view + "/Isolated"
    mb.showinfo(title="Select Processed Image and Image Range", message=dpnd.roi_file_msg)
    file_path = fd.askopenfilename(initialdir=isolated_dir)
    img = cv2.imread(file_path)
    mb.showinfo(title="Isolate Region of Interest", message=dpnd.isolate_roi_msg)
    crop_points(view + '/Isolated', view + '/PreProImages', img)
    range_vals.append(int(input('Please enter the number of the starting image: ')))
    range_vals.append(int(input('Please enter the number of the ending image: ')))

    processed_dir = 'C:/Users/prath/Desktop/ResearchProject/ResearchProject/python_scripts/' + view + "/PreProImages"

    compute.process_images(processed_dir)

    # Handles all thresholding calls
    threshold_callback(view)

    # Get point of interest
    mb.showinfo(title="Select Point of Interest", message=dpnd.poi_msg)
    file_path = fd.askopenfilename(initialdir=processed_dir.replace("PreProImages", "Thresholded"))
    img = cv2.imread(file_path)
    poi = get_poi(img)

    mb.showinfo(title="Reading The Output", message=dpnd.completion_msg)
    done = tk.Button(text='Start contour creation!',
                         command=quit_callback).pack(fill=tk.X)

def threshold_callback(view):
    """Helps user identify threshold range and crop resulting image"""
    global thresh_vals, range_vals, poi, win

    # Get threshold range
    mb.showinfo(title="Identify Threshold Values", message=dpnd.threshold_msg)
    processed_dir = 'C:/Users/prath/Desktop/ResearchProject/ResearchProject/python_scripts/' + view + "/PreProImages"
    file_path = fd.askopenfilename(initialdir=processed_dir)
    img = cv2.imread(file_path)
    get_threshold_vals(img)
    thresh_vals.append(int(input("Please enter the value for the lower threshold: ")))
    thresh_vals.append(int(input("Please enter the value for the upper threshold: ")))

    # Creates red/black images of regions that fall under threshold range
    compute.threshold(view, range_vals, thresh_vals[0], thresh_vals[1])

    # Crop resulting red/black images for final contour creation
    threshold_dir = processed_dir.replace("PreProImages", "Thresholded")
    mb.showinfo(title="Select Thresholded Image", message=dpnd.select_thresh_msg)
    file_path = fd.askopenfilename(initialdir=threshold_dir)
    img = cv2.imread(file_path)
    mb.showinfo(title="Isolate Thresholded Region", message=dpnd.isolate_roi_msg)
    points = crop_points(view + '/Thresholded', view + '/Thresholded', img)


def quit_callback():
    """Callback function to close the main window."""
    global win
    win.quit()


def draw_line_callback(event, x, y, flags, param):
    """Callback function to help user draw lines on image."""
    img = param[0]
    points = param[1]
    # checks for event
    if event == cv2.EVENT_LBUTTONDBLCLK:
        # draws line with new endpoint as selected by user
        cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
        points.append((x, y))
        i = len(points) - 1
        if i > 0:
            cv2.line(img, points[i - 1], points[i], (255, 0, 0), 1)


def crop_points(source_dir, dest_dir, img, orig_flag=False):
    """Creates OpenCV Window with selected image. Isolates selected portion of image in all images."""
    points = []
    param = [img, points]

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_line_callback, param)

    # Display image and run till the escape key is hit
    while 1:
        cv2.imshow('image', img)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()

    if len(points) != 0:
        # Formats user selected points
        for i in range(len(points)):
            points[i] = list(points[i])
        pts = np.array(points)
        points = []

        # Crop the bounding rectangle
        rect = cv2.boundingRect(pts)
        x, y, w, h = rect
        cropped = np.copy(img[y:y + h, x:x + w])

        # Make mask
        pts = pts - pts.min(axis=0)
        mask = np.zeros(cropped.shape[:2], np.uint8)
        cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

        # Apply mask to all images in directory TestImages
        files = os.listdir(source_dir)
        source_dir = source_dir + '/'
        dest_dir = dest_dir + '/'
        for file_name in files:
            file_path = source_dir + file_name
            img_original = cv2.imread(file_path)
            img_original = img_original[y:y + h, x:x + w]
            if '.tif' in file_name:
                file_name = file_name.removesuffix('.tif') + '.png'
            cv2.imwrite(dest_dir + file_name, cv2.bitwise_and(img_original, img_original, mask=mask))
        
        if orig_flag:
            source_dir = source_dir.replace("Thresholded/", "PreProImages")
            dest_dir = dest_dir.replace("Thresholded/", "PreProImages")
            files = os.listdir(source_dir)
            source_dir = source_dir + '/'
            dest_dir = dest_dir + '/'
            for file_name in files:
                file_path = source_dir + file_name
                img_original = cv2.imread(file_path)
                img_original = img_original[y:y + h, x:x + w]
                if '.tif' in file_name:
                    file_name = file_name.removesuffix('.tif') + '.png'
                cv2.imwrite(dest_dir + file_name, cv2.bitwise_and(img_original, img_original, mask=mask))
        return

    # No points were selected, so just write the original image   
    else:
        files = os.listdir(source_dir)
        source_dir = source_dir + '/'
        dest_dir = dest_dir + '/'
        for file_name in files:
            file_path = source_dir + file_name
            img_original = cv2.imread(file_path)
            if '.tif' in file_name:
                file_name = file_name.removesuffix('.tif') + '.png'
            cv2.imwrite(dest_dir + file_name, img_original)
        return []


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
        val = img[y, x][0]
        print("Value: ", val)


def get_poi(img):
    """Creates OpenCV window with selected image. Uses corresponding callback function to show values to user."""
    cv2.namedWindow('image')
    point = []
    param = [img, point]
    cv2.setMouseCallback('image', poi_callback, param)
    while 1:
        cv2.imshow('image', img)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()
    return point


def poi_callback(event, x, y, flags, param):
    """Gets values for parameters through listening for mouse clicks on image window"""
    img = param[0]
    point = param[1]
    # checks for event
    if event == cv2.EVENT_LBUTTONDBLCLK:
        # draws line with new endpoint as selected by user
        cv2.circle(img, (x, y), 4, (255, 0, 0), -1)
        point.append(x)
        point.append(y)


def main():
    """main function"""
    global thresh_vals, range_vals, poi, win

    # Initialize UI window
    view = input("Please enter the MRI perspective (coronal, sagittal, or axial): \n")
    directions = tk.Message(text=dpnd.intro_msg)
    directions.pack()
    start_button = tk.Button(win, text="Start!", command=lambda:start_callback(view))
    start_button.pack()
    win.geometry("700x350")
    win.mainloop()
    win.quit()

    contours = []

    # Runs contour algorithm
    if thresh_vals:
        contours = compute.draw_contours(view, range_vals, poi)
    else:
        print("error")

    # Generates 3d mesh
    compute.create_mesh(view)

if __name__ == '__main__':
    main()

# 6 mm across
# .3 mm depth
