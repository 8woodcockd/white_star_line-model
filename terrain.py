# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:23:01 2018

@author: Dean
"""
global cols_radar
class Ice:
    global cols_radar
    def __init__(self, i, j, radar, lidar, lidar_unit_height, pixel_area, 
                 ice_mass_density, fraction_ice_asl,cols_radar):
        """Assign attributes to each identified ice cell.
        """ 
        self._x = j
        self._y = i
        self.radar = radar[i][j]
        self.lidar = lidar[i][j]
        self.id = 0                          
        self.height = lidar[i][j] * lidar_unit_height         
        self.volume_asl = self.height * pixel_area
        self.volume_tot = self.volume_asl * (1 / fraction_ice_asl)
        self.mass_asl = self.volume_asl * ice_mass_density 
        self.mass_tot = self.mass_asl * (1 / fraction_ice_asl)   
        self.cols_radar = cols_radar
        self.neighbours = []
        self.tug = False
    
    @property
    def x(self):
        if self._x < self.cols_radar:
            return self._x
        else:
            print('The x value is outside of the acceptable range.')
    
    @x.setter
    def x(self, value):
        if isinstance(value, int) == False: 
            print('x value must be integer')
            return
        if 0 <= value <= self.cols_radar:
            self._x = value
        else:
            print('x value entered is outside of the acceptable range')        

    @x.deleter
    def x(self):
        print('You cannot delete the ice.x attributes.')
        return
    
    @property
    def y(self):
        if self._y < self.cols_radar:
            return self._y
        else:
            print('The y value is outside of the acceptable range.')
    
    @y.setter
    def y(self, value):
        if isinstance(value, int) == False: 
            print('y value must be integer')
            return
        if 0 <= value <= self.cols_radar:
            self._y = value
        else:
            print('y value entered is outside of the acceptable range')        

    @y.deleter
    def y(self):
        print('You cannot delete the ice y attributes.')
        return

class Sea:
    """Assign attributes to each identified non-ice cell (assumed sea).
    """
    def __init__(self, i, j, radar, lidar):
        self.x = i
        self.y = j
        self.radar = self
        self.lidar = lidar[i][j]
        

    