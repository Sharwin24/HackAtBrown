
import os
 
dirs = ['/Convex', '/Isolated', '/PreProImages', '/Regular', '/OverlayedConvexImages',  '/OverlayedImages', '/Thresholded']

views = ['coronal', 'sagittal']
for view in views:
    for dir in dirs:
        dir = view + dir
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))