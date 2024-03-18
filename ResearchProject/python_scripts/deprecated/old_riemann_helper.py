from math import floor
import cv2
import numpy as np

class RiemannHelper(object):
    def __init__(self, img, unit_dist):
        green = [0,255,0]
        y, x = np.where(np.all(img==green,axis=2))
        points = []
        for (p1,p2) in zip(x,y): points.append([p1,p2])
        self.point_list = sorted(points, key=lambda x: int(x[0]))
        self.start = self.point_list[0][0]
        self.end = self.point_list[-1][0]
        self.unit_dist = unit_dist
        self.key_points = {}

    def get_key_points(self):
        num_rect = floor((self.end - self.start)/self.unit_dist) - 1
        self.key_points[self.start] = []
        x_coords = [self.start]
        for i in range(0, num_rect + 1):
            x_coords.append(x_coords[-1] + self.unit_dist)
            self.key_points[x_coords[-1]] = []

        for p in self.point_list:
            if p[0] in self.key_points:
                self.key_points[p[0]].append(p[1])
        
        for p in self.key_points:
            self.key_points[p] = [self.key_points[p][0], self.key_points[p][-1]]

        return x_coords
    
    def get_polygons(self):
        x_coords = self.get_key_points()
        polygons = []
        
        for i in range(0, len(x_coords) - 1):   
            curr = x_coords[i]
            next = x_coords[i+1]
            polygons.append([[curr, self.key_points[curr][0]],
                            [next, self.key_points[next][0]],
                            [next, self.key_points[next][1]],
                            [curr, self.key_points[curr][1]]]
                           )

        return polygons

    


    