from math import sqrt, pow
import numpy as np
from mayavi.mlab import *
import os
from contour import Contour
from collections import OrderedDict

class Hexagons(object):
    def __init__(self, dir, unit_dist):
        files = os.listdir(dir)
        self.contour_list = []
        self.unit_dist = unit_dist
        self.evens = OrderedDict()
        self.odds = OrderedDict()
        for file in files:
            path = dir + '/' + file
            self.contour_list.append(Contour(path, unit_dist))

    def add_points(self, points, even_flag):
        if even_flag:
            for p in points:
                self.evens[p] = None
            for i in range(len(points)-1):
                        self.odds[((points[i] + points[i+1])/2)] = None
        else:
            for p in points:
                self.odds[p] = None
            for i in range(len(points)-1):
                        self.evens[((points[i] + points[i+1])/2)] = None

    def get_offset(self, key, point):
        return ((key % self.unit_dist - point % self.unit_dist) % self.unit_dist)

    def format_key_points(self):
        for i in range(len(self.contour_list)):
            contour = self.contour_list[i]
            start = contour.start
            keys = [] 
            coords = []
            even_flag = True
            if i == 0:
                coords = contour.set_key_points()
                self.add_points(coords,even_flag)
            elif i % 2 == 0:
                keys = list(self.evens.keys())    
                if start in self.evens:
                    coords = contour.set_key_points()
            else:
                even_flag = False
                keys = list(self.odds.keys())
                if start in self.odds:
                    coords = contour.set_key_points()
            
            if not coords:
                if start > keys[-1]:
                    offset = self.get_offset(keys[-1], start)
                elif start < keys[0]:
                    offset = self.get_offset(keys[0], start)
                else:
                    counter = 0
                    while keys[counter] < start:
                        counter += 1
                    offset = self.get_offset(keys[counter-1], start)
                coords = contour.set_key_points(inner_start=offset + start)
            self.add_points(coords[1:],even_flag)
            
    def get_measurements(self):
        side_length = self.unit_dist/sqrt(3)
        offset = sqrt(pow(side_length, 2) - pow(self.unit_dist/2, 2))
        return side_length, offset

    def create_mesh(self, view):
        x = []
        y = []
        z = []
        triangles = []
        all_rectangles = []
        count = 0
        side_length, offset = self.get_measurements()
        base = 0
        for contour in self.contour_list:
            hexagons,rectangle = contour.get_polygons(base)
            all_rectangles.extend(rectangle)
            for p in hexagons:
                count += 1
                for l in p:
                    x.append(l[0])
                    y.append(l[1])
                    z.append(l[2])
                p = np.array(p)   
            base = base + side_length + offset    
               
        for i in range(0, count):
            triangles.append((np.array([0,1,2]) + (i * 12)))
            triangles.append((np.array([1,2,3]) + (i * 12)))
            triangles.append((np.array([2,3,4]) + (i * 12)))
            triangles.append((np.array([3,4,5]) + (i * 12)))
            triangles.append((np.array([4,5,6]) + (i * 12)))
            triangles.append((np.array([5,6,7]) + (i * 12)))
            triangles.append((np.array([6,7,8]) + (i * 12)))
            triangles.append((np.array([7,8,9]) + (i * 12)))
            triangles.append((np.array([8,9,10]) + (i * 12)))
            triangles.append((np.array([9,10,11]) + (i * 12)))
            triangles.append((np.array([10,11,0]) + (i * 12)))
            triangles.append((np.array([11,0,1]) + (i * 12)))

        # TODO add Rectangle ends
        # for rectangle in all_rectangles:
        #     for p in rectangle:
        #         for l in p:
        #             x.append(l[0])
        #             y.append(l[1])
        #             z.append(l[2])
        #         p = np.array(p)    
        # for i in range(0, count):
        #     triangles.append((np.array([0,1,2]) + (i * 12)))
        #     triangles.append((np.array([1,2,3]) + (i * 12)))
        #     triangles.append((np.array([2,3,4]) + (i * 12)))
        #     triangles.append((np.array([3,4,5]) + (i * 12)))
        #     triangles.append((np.array([4,5,6]) + (i * 12)))
        #     triangles.append((np.array([5,6,7]) + (i * 12)))
        #     triangles.append((np.array([6,7,8]) + (i * 12)))
        #     triangles.append((np.array([7,8,9]) + (i * 12)))
        #     triangles.append((np.array([8,9,10]) + (i * 12)))
        #     triangles.append((np.array([9,10,11]) + (i * 12)))
        #     triangles.append((np.array([10,11,0]) + (i * 12)))
        #     triangles.append((np.array([11,0,1]) + (i * 12)))
        triangular_mesh(x,y,z,triangles)
        savefig(view + '/figure.obj')
        show()
            


        