# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 19:37:18 2018

@author: Dean
"""
import csv
import math
import terrain
import matplotlib.pyplot
import matplotlib.colors
import numpy

# function used to determine the maximum and minimum values in the radar and 
# lidar datasets.
def max_min(self):
    '''return the maximum and minimum value within the 2D array'''
    max = -math.inf
    min = math.inf
    for row in self:
        for value in row:
            if value > max:
                max = value
            if value < min:
                min = value
    return [max, min]


# load the radar data.
radar = []
with open('white2_radar.txt', newline ='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader: 
        rowlist = []
        for value in row:
            rowlist.append(value)
        radar.append(rowlist)
#calculate the number of x and y values and hence the grid area.
rows_radar = len(radar)
cols_radar = len(radar[0])
#print('number of rows in radar data: ', rows_radar)
#print('number of cols in radar data: ', cols_radar)

# load the lidar data.
lidar = []
with open('white2_lidar.txt', newline ='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader: 
        #print(row)
        rowlist = []
        for value in row:
            rowlist.append(value)
        lidar.append(rowlist)
#calculate the number of x and y values and hence the grid area.
rows_lidar = len(lidar)
cols_lidar = len(lidar[0])
#print('number of rows in lidar data: ', rows_lidar)
#print('number of cols in lidar data: ', cols_lidar)


#return the maximum and minimum values of the radar and lidar files
max_min_radar = max_min(radar)
print('max radar:',max_min_radar[0], 'min radar:',max_min_radar[1])
max_min_lidar = max_min(lidar)
print('max lidar:',max_min_lidar[0], 'min lidar:',max_min_lidar[1])


# classify the terrain of each sq m area in the grid area.
ice = []
sea = []
for i in range (cols_radar):
    for j in range (rows_radar):
        if radar[i][j] >= 100:
            ice.append(terrain.Ice(i, j, radar, lidar))
        else:
            sea.append(terrain.Sea(i, j, radar, lidar))
print('number of cells containing ice:', len(ice))
print('number of cells not containing ice:', len(sea))


'''
fig = matplotlib.pyplot.figure(figsize=(9, 9))
plot = matplotlib.pyplot.imshow(radar)
matplotlib.pyplot.show()
'''
'''
fig = matplotlib.pyplot.figure(figsize=(9, 9))
ax = fig.add_axes([0.05, 0.475, 0.9, 0.15])
# create discrete colourmap
cmap = matplotlib.colors.ListedColormap(['blue', 'green', 'red'])
bounds = [-0.5,0.5,1.5,2.5]
tick = ['','sea','iceburg towable','iceburg not towable']
norm = matplotlib.colors.BoundaryNorm(bounds,cmap.N)
cbar = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap,
                                norm=norm,
                                ticks=bounds,  # optional
                                spacing='proportional',
                                orientation='horizontal')
matplotlib.colorbar.set_label('iceburg plot')
'''
'''
# Define bins that you want, and then classify the data           source:  https://www.earthdatascience.org/courses/earth-analytics-python/lidar-raster-data/classify-plot-raster-data-in-python/
class_bins = [0, 36000000, math.inf]

# You'll classify the original image array, then unravel it again for plotting
mass_class = numpy.digitize(mass, class_bins)

# Note that you have an extra class in the data (0)
print(numpy.unique(lidar_chm_im_class))
'''


# search cells around each ice cell and append to it's list of neighbours any ice celLs to the N, E, W, S.
for i in range(len(ice)):
    ice[i].neighbours = []
    for j in range (len(ice)):
        # cell to the west
        if (ice[j].x == (ice[i].x - 1)) & (ice[j].y == ice[i].y):  
            ice[i].neighbours.append(ice[j])
        # cell to the north
        elif (ice[j].x == ice[i].x) & (ice[j].y == (ice[i].y - 1)):  
            ice[i].neighbours.append(ice[j])
        # cell to the east
        elif (ice[j].x == ice[i].x + 1) & (ice[j].y == (ice[i].y)):  
            ice[i].neighbours.append(ice[j])
        # cell to the north
        elif (ice[j].x == ice[i].x) & (ice[j].y == (ice[i].y + 1)):  
            ice[i].neighbours.append(ice[j])   
            #id += 1

#this should loop through all ice not in checked list and keep adding the neighbours to 
#check to the to_check list and keep working through the ice in the to 
#check list until it is empty.    

id = 0
num_of_icebergs = 0
checked = []
to_check = []
for i in range(len(ice)):   
    if ice[i] not in checked:
        id += 1
        ice[i].id = id
        checked.append(ice[i])
        if ice[i] in to_check:
            to_check.remove(ice[i])
        for j in range(len(ice[i].neighbours)):
            to_check.append(ice[i].neighbours[j])
        #print('are there two nested lists?', to_check)
        while len(to_check) > 0:
            #print('len(to_check) > 0')
            to_check[0].id = id       # key line
            for j in range(len(to_check[0].neighbours)):
                if (to_check[0].neighbours[j] not in checked) & (to_check[0].neighbours[j] not in to_check):
                    to_check.append(to_check[0].neighbours[j])
            checked.append(to_check[0])
            to_check.remove(to_check[0])

num_of_icebergs = id
print('number of icebergs:',num_of_icebergs)

# calculate the total mass of all icebergs.    
total_iceburg_mass = 0
for i in range(len(ice)):
    total_iceburg_mass += ice[i].mass_tot
print('total_iceburg_mass:',total_iceburg_mass)

iceberg_mass = []
for i in range(num_of_icebergs):
    berg_mass = 0
    for j in range (len(ice)):
        if ice[j].id == i + 1:
            berg_mass += ice[j].mass_tot
    iceberg_mass.append(berg_mass)
print(iceberg_mass)

for i in range(num_of_icebergs):
    if iceberg_mass[i] < 36000000:
        print('Iceberg ' + str(i + 1) + ' can be tugged')
    else:
        print('Iceberg ' + str(i + 1) + ' cannot be tugged')

print('\nmodel complete')