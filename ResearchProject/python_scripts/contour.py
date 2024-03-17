from math import floor, sqrt, pow
import cv2
import numpy as np
from mayavi.mlab import *
import os


class Contour(object):
    def __init__(self, path, unit_dist):
        img = cv2.imread(path)
        green = [0,255,0]
        y, x = np.where(np.all(img==green,axis=2))
        points = []
        for (p1,p2) in zip(x,y): points.append([p1,p2])
        self.point_list = sorted(points, key=lambda x: int(x[0]))
        self.start = self.point_list[0][0]
        self.end = self.point_list[-1][0]
        self.unit_dist = unit_dist
        self.key_points = {}
        self.x_coords = []

    def set_key_points(self, inner_start=0):
        num_rect = floor((self.end - self.start)/self.unit_dist) - 1
        self.key_points[self.start] = []
        x_coords = [self.start]
        if not inner_start:
            for i in range(0, num_rect + 1):
                x_coords.append(x_coords[-1] + self.unit_dist)
                self.key_points[x_coords[-1]] = []
        else:
            self.key_points[inner_start] = []
            x_coords.append(inner_start)
            for i in range(0, num_rect):
                x_coords.append(x_coords[-1] + self.unit_dist)
                self.key_points[x_coords[-1]] = []

        for i in range(1, len(x_coords) - 1):
            self.key_points[(x_coords[i] + x_coords[i+1])/2] = []

        for p in self.point_list:
            if p[0] in self.key_points:
                self.key_points[p[0]].append(p[1])

        for p in self.key_points:
            self.key_points[p] = [self.key_points[p][0], self.key_points[p][-1]]

        self.x_coords = x_coords
        return x_coords

    def get_measurements(self):
        side_length = self.unit_dist/sqrt(3)
        offset = sqrt(pow(side_length, 2) - pow(self.unit_dist/2, 2))
        return side_length, offset

    def get_polygons(self, base):
        x_coords = self.x_coords
        hexagons = []
        side_length, offset = self.get_measurements()
        for i in range(1, len(x_coords) - 1):   
            curr = x_coords[i]
            next = x_coords[i+1]
            hexagons.append([[curr, self.key_points[curr][0], base + offset],
                            [curr, self.key_points[curr][1], base + offset],
                            [(curr + next)/2, self.key_points[(curr + next)/2][0], base],
                            [(curr + next)/2, self.key_points[(curr + next)/2][1], base],
                            [next, self.key_points[next][0], base + offset],
                            [next, self.key_points[next][1], base + offset],
                            [next, self.key_points[next][0], base + side_length + offset],
                            [next, self.key_points[next][1], base + side_length + offset],
                            [(curr + next)/2, self.key_points[(curr + next)/2][0], base + side_length + 2 * offset],
                            [(curr + next)/2, self.key_points[(curr + next)/2][1], base + side_length + 2 * offset],
                            [curr, self.key_points[curr][0], base + side_length + offset],
                            [curr, self.key_points[curr][1], base + side_length + offset]]
                        )
        rectangle = [[x_coords[0], self.key_points[x_coords[0]][0], base + offset],
                            [x_coords[0], self.key_points[x_coords[0]][1], base + offset],
                            [x_coords[1], self.key_points[x_coords[1]][0], base + offset],
                            [x_coords[1], self.key_points[x_coords[1]][1], base + offset],
                            [x_coords[0], self.key_points[x_coords[0]][0], base + offset + side_length],
                            [x_coords[0], self.key_points[x_coords[0]][1], base + offset + side_length],
                            [x_coords[1], self.key_points[x_coords[1]][0], base + offset + side_length],
                            [x_coords[1], self.key_points[x_coords[1]][1], base + offset + side_length],
                            ]
        return hexagons, rectangle