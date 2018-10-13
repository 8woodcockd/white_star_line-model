# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:23:01 2018

@author: Dean
"""

class Ice:
    
    def __init__(self, i, j, radar, lidar, lidar_unit_height, pixel_area, 
                 ice_mass_density, fraction_ice_asl, cols_radar):
        """Assign attributes to each identified ice cell.
        """ 
        self._x = j
        self._y = i
        self._radar = radar[i][j]
        self._lidar = lidar[i][j]
        self._id = 0                          
        self._height = lidar[i][j] * lidar_unit_height         
        self._volume_asl = self.height * pixel_area
        self._volume_tot = self.volume_asl * (1 / fraction_ice_asl)
        self._mass_asl = self.volume_asl * ice_mass_density 
        self._mass_tot = self.mass_asl * (1 / fraction_ice_asl)   
        self._cols_radar = cols_radar
        self._neighbours = []
        self._tug = False
    
    @property
    def x(self):
        """Specify the conditions to get_x.
        """
        if self._x < self._cols_radar:
            return self._x
        else:
            print('The x value is outside of the acceptable range.')
    
    @x.setter
    def x(self, value):
        """Specify the conditions to set_x.
        """
        if isinstance(value, int) == False: 
            print('x value must be integer')
            return
        if 0 <= value <= self._cols_radar:
            self._x = value
        else:
            print('x value entered is outside of the acceptable range')        

    @x.deleter
    
    def x(self):
        """Specify the conditions to del_x.
        """
        print('You cannot delete the ice.x attributes.')
        return
    
    @property
    def y(self):
        """Specify the conditions to get_y.
        """
        if self._y < self._cols_radar:
            return self._y
        else:
            print('The y value is outside of the acceptable range.')
    
    @y.setter
    def y(self, value):
        """Specify the conditions to set_y.
        """
        if isinstance(value, int) == False: 
            print('y value must be integer')
            return
        if 0 <= value <= self._cols_radar:
            self._y = value
        else:
            print('y value entered is outside of the acceptable range')        

    @y.deleter
    def y(self):
        """Specify the conditions to del_y.
        """
        print('You cannot delete the ice y attributes.')
        return
    
    @property
    def radar(self):
        """Specify the conditions to get_radar.
        """
        return self._radar
    
    @radar.setter
    def radar(self, value):
        """Specify the conditions to set_radar.
        """
        self._radar = value

    @radar.deleter
    def radar(self):
        """Specify the conditions to del_radar.
        """
        print('You cannot delete the radar attribute.')
        return
    
    @property
    def lidar(self):
        """Specify the conditions to get_lidar.
        """
        return self._lidar
   
    @lidar.setter
    def lidar(self, value):
        """Specify the conditions to set_lidar.
        """
        self._lidar = value

    @lidar.deleter
    def lidar(self):
        """Specify the conditions to del_lidar.
        """
        print('You cannot delete the lidar attribute.')
        return
    
    @property
    def id(self):
        """Specify the conditions to get_id.
        """
        return self._id
   
    @id.setter
    def id(self, value):
        """Specify the conditions to set_id.
        """
        if self._id > 0:
            print('Cannot change iceberg ID.')
        else:
            self._id = value

    @id.deleter
    def id(self):
        """Specify the conditions to del_id.
        """
        print('You cannot delete the iceberg ID.')
        return

    @property
    def height(self):
        """Specify the conditions to get_height.
        """
        return self._height
   
    @height.setter
    def height(self, value):
        """Specify the conditions to set_height.
        """
        self._height = value

    @height.deleter
    def height(self):
        """Specify the conditions to del_height.
        """
        print('You cannot delete the height attribute.')
        return

    @property
    def volume_asl(self):
        """Specify the conditions to get_volume_asl.
        """
        return self._volume_asl
   
    @volume_asl.setter
    def volume_asl(self, value):
        """Specify the conditions to set_volume_asl.
        """
        self._volume_asl = value

    @volume_asl.deleter
    def volume_asl(self):
        """Specify the conditions to del_volume_asl.
        """
        print('You cannot delete the volume_asl attribute.')
        return
    
    @property
    def volume_tot(self):
        """Specify the conditions to get_volume_tot.
        """
        return self._volume_tot
   
    @volume_tot.setter
    def volume_tot(self, value):
        """Specify the conditions to set_volume_tot.
        """
        self._volume_tot = value

    @volume_tot.deleter
    def volume_tot(self):
        """Specify the conditions to del_volume_tot.
        """
        print('You cannot delete the volume_tot attribute.')
        return
    
    @property
    def mass_asl(self):
        """Specify the conditions to get_mass_asl.
        """
        return self._mass_asl
   
    @mass_asl.setter
    def mass_asl(self, value):
        """Specify the conditions to set_mass_asl.
        """
        self._mass_asl = value

    @mass_asl.deleter
    def mass_asl(self):
        """Specify the conditions to del_mass_asl.
        """
        print('You cannot delete the mass_asl attribute.')
        return
    
    @property
    def mass_tot(self):
        """Specify the conditions to get_mass_tot.
        """
        return self._mass_tot
   
    @mass_tot.setter
    def mass_tot(self, value):
        """Specify the conditions to set_mass_tot.
        """
        self._mass_tot = value

    @mass_tot.deleter
    def mass_tot(self):
        """Specify the conditions to del_mass_tot.
        """
        print('You cannot delete the mass_tot attribute.')
        return

    @property
    def cols_radar(self):
        """Specify the conditions to get_cols_radar.
        """
        return self._cols_radar
    
    @cols_radar.setter
    def cols_radar(self, value):
        """Specify the conditions to set_cols_radar.
        """
        self._cols_radar = value

    @cols_radar.deleter
    def cols_radar(self):
        """Specify the conditions to del_cols_radar.
        """
        print('You cannot delete the cols_radar attribute.')
        return
    
    @property
    def neighbours(self):
        """Specify the conditions to get_neighbours.
        """
        return self._neighbours
   
    @neighbours.setter
    def neighbours(self, value):
        """Specify the conditions to set_neighbours.
        """
        print('Cannot change neighbours attribute.')

    @neighbours.deleter
    def neighbours(self):
        """Specify the conditions to del_neighbours.
        """
        print('You cannot delete the neighbours attribute.')
        return
    
    @property
    def tug(self):
        """Specify the conditions to get_tug.
        """
        return self._tug
   
    @tug.setter
    def tug(self, value):
        """Specify the conditions to set_tug.
        """
        if self._tug > 0:
            print('Cannot change the assigned tug attribute.')
        self._tug = value

    @tug.deleter
    def tug(self):
        """Specify the conditions to del_tug.
        """
        print('You cannot delete the tug attribute.')
        return
    
class Sea:
    """Assign attributes to each identified non-ice cell (assumed sea).
    """
    def __init__(self, i, j, radar, lidar):
        """Assign attributes to each identified ice cell.
        """ 
        self._x = i
        self._y = j
        self._radar = self
        self._lidar = lidar[i][j]
        
    @property
    def x(self):
        """Specify the conditions to get_x.
        """
        if self._x < self._cols_radar:
            return self._x
        else:
            print('The x value is outside of the acceptable range.')
   
    @x.setter
    def x(self, value):
        """Specify the conditions to set_x.
        """
        if isinstance(value, int) == False: 
            print('x value must be integer')
            return
        if 0 <= value <= self._cols_radar:
            self._x = value
        else:
            print('x value entered is outside of the acceptable range') 

    @x.deleter
    def x(self):
        """Specify the conditions to del_x.
        """
        print('You cannot delete the x attribute.')
        return
    
    @property
    def y(self):
        """Specify the conditions to get_y.
        """
        if self._y < self._cols_radar:
            return self._y
        else:
            print('The y value is outside of the acceptable range.')
   
    @y.setter
    def y(self, value):
        """Specify the conditions to set_y.
        """
        if isinstance(value, int) == False: 
            print('y value must be integer')
            return
        if 0 <= value <= self._cols_radar:
            self._y = value
        else:
            print('y value entered is outside of the acceptable range')  

    @y.deleter
    def y(self):
        """Specify the conditions to del_y.
        """
        print('You cannot delete the y attribute.')
        return
    
    @property
    def radar(self):
        """Specify the conditions to get_radar.
        """
        return self._radar
    
    @radar.setter
    def radar(self, value):
        """Specify the conditions to set_radar.
        """
        self._radar = value

    @radar.deleter
    def radar(self):
        """Specify the conditions to del_radar.
        """
        print('You cannot delete the radar attribute.')
        return
    
    @property
    def lidar(self):
        """Specify the conditions to get_lidar.
        """
        return self._lidar
   
    @lidar.setter
    def lidar(self, value):
        """Specify the conditions to set_lidar.
        """
        self._lidar = value

    @lidar.deleter
    def lidar(self):
        """Specify the conditions to del_lidar.
        """
        print('You cannot delete the lidar attribute.')
        return
    
    