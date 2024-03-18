intro_msg = """Welcome to the lesion drawing script!\nInformation windows will show you the steps you need to follow in order to see the final contours.
Buttons, text input, and other forms of interaction will show up on this window.\nStart by pressing the start button!\n"""

file_msg = """ Press the \"open file\" button in order to select the base image"""

isolate_sc_msg = """In the OpenCV image that will open, please trace around the spinal cord. Double click on the image to draw a point.\n
As you draw points, lines will be created to connect them. When you have your desired tracing, please hit the escape key to move on.\n
After you finish, please give some time for the isolation algorithm to be applied to all the test images."""

roi_file_msg = """ Please select the image on which you would like to trace the region of interest.\n
Additionally, please select a starting image number and ending number. The first image is considered image 0. You will enter these numbers later."""

select_thresh_msg = """ Please select the thresholded image on which you would like to trace the region of interest.\n"""

isolate_roi_msg = """In the OpenCV image that will open, please trace around the region of interest. Double click on the image to draw a point.\n
As you draw points, lines will be created to connect them. When you have your desired tracing, please hit the escape key to move on.\n"""

bounding_msg = """In the OpenCV image that will open, please identify the upper and lower values for the region of interest.\n 
We will do this by clicking around on the base image. Double left click on the image to see the grayscale value at the point of the click.\n
You will enter these values in the command line shortly. When you have identified the desired values, please hit the escape key to move on."""

poi_msg = """In the OpenCV image that will open, please identify the point of interest.\n 
You will do this by double clicking at the point in the image you believe is the center of the hurt area."""

completion_msg = """Thanks for using the script! It will now output four sets of different images in separate folders.\n
New Images: This directory will contain the standard contours (in green) that are drawn around the thresholded lesions (in red).\n
Overlayed Images: This directory contains the same standard contours as the New Images but they are drawn around the lesions in the original images.\n
Convex: This directory contains convexed contours (in green) that are drawn around the thresholded lesions (in red). \n
Overlayed Convex Images: This directory contains the same standard contours as the Convex Images but they are drawn around the lesions in the original images.\n
To start the contour drawings, please press the \"Start contour creation!\" button on the main screen. Your images will be outputted shortly!"""


