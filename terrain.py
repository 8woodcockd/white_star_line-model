# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:23:01 2018

@author: Dean
"""

class Ice:
    """Assign attributes to each identified ice cell (assumed sea).
    """ 
    
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
        """The x position (easting). Specify the conditions to get_x, set_x,
        and del_x.
        """
        if self._x < self._cols_radar:
            return self._x
        else:
            print('The x value is outside of the acceptable range.')
    @x.setter
    def x(self, value):
        if isinstance(value, int) == False: 
            print('x value must be integer')
            return
        if 0 <= value <= self._cols_radar:
            self._x = value
        else:
            print('x value entered is outside of the acceptable range')        
    @x.deleter
    def x(self):
        print('You cannot delete the ice.x attributes.')
        return
    
    @property
    def y(self):
        """The y position (northing). Specify the conditions to get_y, 
        the conditions to set_y and the conditions to del_y.
        """
        if self._y < self._cols_radar:
            return self._y
        else:
            print('The y value is outside of the acceptable range.')
    @y.setter
    def y(self, value):
        if isinstance(value, int) == False: 
            print('y value must be integer')
            return
        if 0 <= value <= self._cols_radar:
            self._y = value
        else:
            print('y value entered is outside of the acceptable range')        
    @y.deleter
    def y(self):
        print('You cannot delete the ice y attributes.')
        return
    
    @property
    def radar(self):
        """The radar value associated with the ice cell. Specify the conditions
        to get_radar, set_radar, and del_radar.
        """
        return self._radar
    @radar.setter
    def radar(self, value):
        self._radar = value
    @radar.deleter
    def radar(self):
        print('You cannot delete the radar attribute.')
        return
    
    @property
    def lidar(self):
        """The lidar value associated with the ice cell. Specify the conditions
        to get_lidar, set_lidar, and del_lidar.
        """
        return self._lidar
    @lidar.setter
    def lidar(self, value):
        self._lidar = value
    @lidar.deleter
    def lidar(self):
        print('You cannot delete the lidar attribute.')
        return
    
    @property
    def id(self):
        """The identification number given to each cell of ice to specify which 
        iceberg it is associated with. Specify the conditions to get_id, the
        conditions to set_id, and the conditions to del_id
        """
        return self._id
    @id.setter
    def id(self, value):
        if self._id > 0:
            print('Cannot change iceberg ID.')
        else:
            self._id = value
    @id.deleter
    def id(self):
        print('You cannot delete the iceberg ID.')
        return

    @property
    def height(self):
        """The height of the ice above sea level. Specify the conditions to
        get_height, the conditions to set_height, and the conditions to 
        del_height.
        """
        return self._height
    @height.setter
    def height(self, value):
        self._height = value
    @height.deleter
    def height(self):
        print('You cannot delete the height attribute.')
        return

    @property
    def volume_asl(self):
        """The volume of ice above sea level at the specified terrain position 
        (raster cell). Specify the conditions to get_volume_asl,  the
        conditions to set_volume_asl, and the conditions to del_volume_asl. 
        """
        return self._volume_asl
    @volume_asl.setter
    def volume_asl(self, value):
        self._volume_asl = value
    @volume_asl.deleter
    def volume_asl(self):
        print('You cannot delete the volume_asl attribute.')
        return
    
    @property
    def volume_tot(self):
        """The total volume of ice above and below sea level at the specified
        terrain position (raster cell). Specify the conditions to 
        get_volume_tot, the conditions to set_volume_tot, and the conditions to 
        del_volume_tot.
        """
        return self._volume_tot
    @volume_tot.setter
    def volume_tot(self, value):
        self._volume_tot = value
    @volume_tot.deleter
    def volume_tot(self):
        print('You cannot delete the volume_tot attribute.')
        return
    
    @property
    def mass_asl(self):
        """The mass of ice above sea level at the specified terrain position 
        (raster cell). Specify the conditions to get_mass_asl,  the
        conditions to set_mass_asl, and the conditions to del_mass_asl. 
        """
        return self._mass_asl
    @mass_asl.setter
    def mass_asl(self, value):
        self._mass_asl = value
    @mass_asl.deleter
    def mass_asl(self):
        print('You cannot delete the mass_asl attribute.')
        return
    
    @property
    def mass_tot(self):
        """The total mass of ice above and below sea level at the specified
        terrain position (raster cell). Specify the conditions to 
        get_mass_tot, the conditions to set_mass_tot, and the conditions to 
        del_mass_tot.
        """
        return self._mass_tot
    @mass_tot.setter
    def mass_tot(self, value):
        self._mass_tot = value
    @mass_tot.deleter
    def mass_tot(self):
        print('You cannot delete the mass_tot attribute.')
        return

    @property
    def cols_radar(self):
        """The number of columns in the raster grid of the radar data (the 
        lidar data should have the same number of columns). Specify the 
        conditions to get_cols_radar, set_cols_radar, and del_cols_radar.
        """
        return self._cols_radar
    @cols_radar.setter
    def cols_radar(self, value):
        self._cols_radar = value
    @cols_radar.deleter
    def cols_radar(self):
        print('You cannot delete the cols_radar attribute.')
        return
    
    @property
    def neighbours(self):
        """A list of the adjacent ice cells in the raster grid. Specify the
        conditions to get_neighbours, set_neighbours, and del_neighbours.
        """
        return self._neighbours
    @neighbours.setter
    def neighbours(self, value):
        print('Cannot change neighbours attribute.')
    @neighbours.deleter
    def neighbours(self):
        print('You cannot delete the neighbours attribute.')
        return
    
    @property
    def tug(self):
        """A boolean property which identifies whether the ice cell is part of
        an iceberg that can be tugged. Specify the conditions to get_tug, 
        set_tug, and del_tug.
        """
        return self._tug
    @tug.setter
    def tug(self, value):
        if self._tug > 0:
            print('Cannot change the assigned tug attribute.')
        self._tug = value
    @tug.deleter
    def tug(self):
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
        """The x position (easting). Specify the conditions to get_x, set_x,
        and del_x.
        """
        if self._x < self._cols_radar:
            return self._x
        else:
            print('The x value is outside of the acceptable range.')
    @x.setter
    def x(self, value):
        if isinstance(value, int) == False: 
            print('x value must be integer')
            return
        if 0 <= value <= self._cols_radar:
            self._x = value
        else:
            print('x value entered is outside of the acceptable range') 
    @x.deleter
    def x(self):
        print('You cannot delete the x attribute.')
        return
    
    @property
    def y(self):
        """The y position (northing). Specify the conditions to get_y, 
        the conditions to set_y and the conditions to del_y.
        """
        if self._y < self._cols_radar:
            return self._y
        else:
            print('The y value is outside of the acceptable range.')
    @y.setter
    def y(self, value):
        if isinstance(value, int) == False: 
            print('y value must be integer')
            return
        if 0 <= value <= self._cols_radar:
            self._y = value
        else:
            print('y value entered is outside of the acceptable range')  
    @y.deleter
    def y(self):
        print('You cannot delete the y attribute.')
        return
    
    @property
    def radar(self):
        """The radar value associated with the sea cell. Specify the conditions
        to get_radar, set_radar, and del_radar.
        """
        return self._radar
    @radar.setter
    def radar(self, value):
        self._radar = value
    @radar.deleter
    def radar(self):
        print('You cannot delete the radar attribute.')
        return
    
    @property
    def lidar(self):
        """The lidar value associated with the sea cell. Specify the conditions
        to get_lidar, set_lidar, and del_lidar.
        """
        return self._lidar
    @lidar.setter
    def lidar(self, value):
        self._lidar = value
    @lidar.deleter
    def lidar(self):
        print('You cannot delete the lidar attribute.')
        return
    
    