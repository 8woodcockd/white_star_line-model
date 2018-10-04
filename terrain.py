# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:23:01 2018

@author: Dean
"""

class Ice:
    
    def __init__(self, i, j, radar, lidar, lidar_unit_height, pixel_area, 
                 ice_mass_density, fraction_ice_asl):
        self.x = j
        self.y = i
        self.radar = radar[i][j]
        self.lidar = lidar[i][j]
        self.id = 0                          
        self.height = lidar[i][j] * lidar_unit_height         
        self.volume_asl = self.height * pixel_area
        self.volume_tot = self.volume_asl * (1 / fraction_ice_asl)
        self.mass_asl = self.volume_asl * ice_mass_density 
        self.mass_tot = self.mass_asl * (1 / fraction_ice_asl)   

        self.neighbours = []
        self.tug = False

class Sea:
    
    def __init__(self, i, j, radar, lidar):
        self.x = i
        self.y = j
        self.radar = self
        self.lidar = lidar[i][j]
        

    