from ctypes.wintypes import PSIZE
import cv2
import numpy as np
from deprecated.old_riemann_helper import RiemannHelper
import os
from mayavi.mlab import *

view = input('Enter view:')
dir = view + '/Convex'
print(dir)
files = os.listdir(dir)
x = []
y = []
z = []
triangles = []
depth = 0
count = 0
for file in files:
    path = dir + '/' + file
    img = cv2.imread(path)
    rh = RiemannHelper(img, 10)
    polygons = rh.get_polygons()
    for p in polygons:
        count += 1
        for l in p:
            x.append(l[0])
            y.append(l[1])
            z.append(depth)
            x.append(l[0])
            y.append(l[1])
            z.append(depth + 7.5)
        p = np.array(p)
        cv2.polylines(img,[p],1,(255,0,0),1)        
    depth += 7.5


for i in range(0, count):
    triangles.append((np.array([0,4,6]) + (i * 8)))
    triangles.append((np.array([0,2,4]) + (i * 8)))
    triangles.append((np.array([0,1,6]) + (i * 8)))
    triangles.append((np.array([1,6,7]) + (i * 8)))
    triangles.append((np.array([1,3,5]) + (i * 8)))
    triangles.append((np.array([1,5,7]) + (i * 8)))
    triangles.append((np.array([2,3,4]) + (i * 8)))
    triangles.append((np.array([3,4,5]) + (i * 8)))

# triangular_mesh(x,y,z,triangles, color = (1,1,1))
triangular_mesh(x,y,z,triangles)
savefig('triangles.obj')
show()
