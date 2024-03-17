import numpy as np
import cv2
import os

def main(view):
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

    

if __name__ == '__main__':
    view = input("enter view\n")
    main(view)



 