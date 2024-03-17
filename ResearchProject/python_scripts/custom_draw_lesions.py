# Dependencies
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import ui_dependencies as dpnd
import cv2
import numpy as np
import os
import compute
import copy

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
# Global variables
bounds = []
range_vals = []
poi = []
temp_view = ''
win = ctk.CTk()
BASE_PATH = 'C:/Users/prath/Desktop/ResearchProject/ResearchProject/python_scripts/'

def start_callback(view):
    """Callback function for the start button. Asks user to use default or custom parameters."""
    mb.showinfo(title="Select Base Image", message=dpnd.file_msg)
    file_select = ctk.CTkButton(master=win, text='Open File',
                            command=lambda:parameter_callback(view)).pack(pady=50)


def parameter_callback(view):
    """Callback function that guides user with selecting parameter values."""
    global bounds, range_vals, poi, win

    win.update()
    # Gets a base image and asks user to trace spinal cord
    base_dir = BASE_PATH + view + "/TestImages"
    file_path = fd.askopenfilename(initialdir=base_dir)
    img = cv2.imread(file_path)
    mb.showinfo(title="Isolate Spinal Cord", message=dpnd.isolate_sc_msg)
    crop_points(view + '/TestImages', view + '/Isolated', img)

    # Shows user isolated spinal cords and asks them to trace around the region of interest
    isolated_dir = BASE_PATH + view + "/Isolated"
    mb.showinfo(title="Select Processed Image and Image Range", message=dpnd.roi_file_msg)
    file_path = fd.askopenfilename(initialdir=isolated_dir)
    img = cv2.imread(file_path)
    mb.showinfo(title="Isolate Region of Interest", message=dpnd.isolate_roi_msg)
    crop_points(view + '/Isolated', view + '/PreProImages', img)

    dialog = ctk.CTkInputDialog(text="Please enter the number of the starting image:", title="Starting Number")
    start = dialog.get_input()
    dialog = ctk.CTkInputDialog(text="Please enter the number of the ending image:", title="Ending Number")
    end = dialog.get_input()
    range_vals.append(int(start))
    range_vals.append(int(end))

    processed_dir = BASE_PATH + view + "/PreProImages"

    compute.process_images(processed_dir)

    # Handles all bounding calls
    bounding(view)

    # Get point of interest
    mb.showinfo(title="Select Point of Interest", message=dpnd.poi_msg)
    file_path = fd.askopenfilename(initialdir=processed_dir.replace("PreProImages", "Thresholded"))
    img = cv2.imread(file_path)
    poi = get_poi(img)

    mb.showinfo(title="Reading The Output", message=dpnd.completion_msg)
    done = ctk.CTkButton(master=win,text='Start contour creation!',
                         command=quit_callback).pack(pady=20)

def bounding(view):
    """Helps user identify bounds range and crop resulting image"""
    global bounds, range_vals, poi, win

    # Get bounds
    mb.showinfo(title="Identify Bound Values", message=dpnd.bounding_msg)
    processed_dir = BASE_PATH + view + "/PreProImages"
    file_path = fd.askopenfilename(initialdir=processed_dir)
    img = cv2.imread(file_path)
    get_bounds(img)

    dialog = ctk.CTkInputDialog(text="Please enter the value for the lower bound:", title="Lower Bound")
    lower = dialog.get_input()
    dialog = ctk.CTkInputDialog(text="Please enter the value for the upper bound:", title="Upper Bound")
    upper = dialog.get_input()
    bounds.append(int(lower))
    bounds.append(int(upper))

    # Creates red/black images of regions that fall under bounds
    compute.threshold(view, range_vals, bounds[0], bounds[1])

    # Crop resulting red/black images for final contour creation
    threshold_dir = processed_dir.replace("PreProImages", "Thresholded")
    mb.showinfo(title="Select Thresholded Image", message=dpnd.select_thresh_msg)
    file_path = fd.askopenfilename(initialdir=threshold_dir)
    img = cv2.imread(file_path)
    mb.showinfo(title="Isolate Thresholded Region", message=dpnd.isolate_roi_msg)
    points = crop_points(view + '/Thresholded', view + '/Thresholded', img)


def get_bounds(img):
    """Creates OpenCV window with selected image. Uses corresponding callback function to show values to user."""
    cv2.namedWindow('image')
    param = [img]
    cv2.setMouseCallback('image', bound_vals_callback, param)
    while 1:
        cv2.imshow('image', img)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


def bound_vals_callback(event, x, y, flags, param):
    """Gets values for parameters through listening for mouse clicks on image window"""
    img = param[0]

    # checks event for single click of right mouse button, printing the grayscale value at the point of the click
    if event == cv2.EVENT_LBUTTONDBLCLK:
        val = img[y, x][0]
        print("Value: ", val)

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

def menu_callback(choice):
    global temp_view
    temp_view = choice
    
def main():
    """main function"""
    global bounds, range_vals, poi, win, temp_view

    view_window = ctk.CTkToplevel()
    view_window.geometry('300x250')
    view_directions = ctk.CTkLabel(master=view_window,text="Please enter the MRI perspective.\n After your selection, close the window to continue.\n")
    view_directions.pack()
    view_box = ctk.CTkOptionMenu(master=view_window, values=['coronal', 'sagittal', 'axial'], command=menu_callback)
    view_box.set('')
    view_box.pack()
    directions = ctk.CTkLabel(master=win,text=dpnd.intro_msg)
    directions.pack()
    start_button = ctk.CTkButton(master=win, text="Start!", command=lambda:start_callback(temp_view))
    start_button.pack()
    win.geometry("600x350")
    win.mainloop()
    win.quit()

    # Runs contour algorithm
    if bounds:
        compute.draw_contours(temp_view, range_vals, poi)
    else:
        print("error")

    # Generates 3d mesh
    compute.create_mesh(temp_view)

if __name__ == '__main__':
    main()

# 6 mm across
# .3 mm depth
