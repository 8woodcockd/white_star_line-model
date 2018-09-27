# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:23:01 2018

@author: Dean
"""

class Ice:
    
    def __init__(self, i, j, radar, lidar):
        self.x = i
        self.y = j
        self.radar = radar[i][j]
        self.lidar = lidar[i][j]
        self.id = 0                          # iceburg ID number
        self.height = lidar[i][j] * 0.1         #1 lidar unit = 0.1m height
        self.mass_asl = self.height * 1 * 900   # height * area * mass per m^3 
        self.mass_tot = self.mass_asl * 10    # approx. 90% of iceberg below sl
        self.neighbours = []
        self.tug = False

class Sea:
    
    def __init__(self, i, j, radar, lidar):
        self.x = i
        self.y = j
        self.radar = self
        self.lidar = lidar[i][j]
        

    