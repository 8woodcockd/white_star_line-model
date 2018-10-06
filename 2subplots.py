# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 15:20:12 2018

@author: Dean
"""
import csv
import matplotlib.pyplot
import matplotlib.colors
from mpl_toolkits.axes_grid1 import make_axes_locatable

filename1 = 'white2_radar.txt'
filename2 = 'white2_lidar.txt'
radar = []
#with open('white2_radar.txt', newline ='') as f:
with open(filename1, newline ='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader: 
        rowlist = []
        for value in row:
            rowlist.append(value)
        radar.append(rowlist)
            
lidar = []
with open(filename2, newline ='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader: 
        #print(row)
        rowlist = []
        for value in row:
            rowlist.append(value)
        lidar.append(rowlist)

rows_radar = len(radar)
cols_radar = len(radar[0])



# Two subplots to display input radar and lidar data
fig, (ax1, ax2) = matplotlib.pyplot.subplots(1, 2)
fig.suptitle('Input Radar and Lidar Data')
#ax1.plot(x, y)

c1 = ax1.imshow(radar, cmap=matplotlib.pyplot.cm.get_cmap('Blues'))
ax1.set_title('Radar:', x = 0, y = 1.08, ha='left')
ax1.set_ylabel('Distance (m)')
ax1.tick_params(labelbottom=False,labeltop=True,top = True, right = True)
# customised x-label definition and position
ax1.text((cols_radar / 2),-20,'Distance (m)',fontsize=10,
        horizontalalignment='center',verticalalignment='center')

c2 = ax2.imshow(lidar, cmap=matplotlib.pyplot.cm.get_cmap('Reds'))
ax2.set_title('Lidar:', x = 0, y = 1.08, ha='left')
ax2.set_ylabel('Distance (m)')
ax2.tick_params(labelbottom=False,labeltop=True,top = True, right = True)
# customised y-label definition and position
ax2.text((cols_radar / 2),-20,'Distance (m)',fontsize=10,
        horizontalalignment='center',verticalalignment='center')


divider = make_axes_locatable(ax1)
cax = divider.append_axes('bottom', size='5%', pad=0.1)
cbar1 = fig.colorbar(c1,orientation="horizontal", cax = cax)
#fig.colorbar(c1, orientation="horizontal", pad=0.2)
cbar1.set_label('Value (0-255)', rotation=0, labelpad=10)

divider = make_axes_locatable(ax2)
cax = divider.append_axes('bottom', size='5%', pad=0.1)
cbar2 = fig.colorbar(c2,orientation="horizontal", cax = cax)
#fig.colorbar(c2, orientation="horizontal", pad=0.2)
cbar2.set_label('Value (0-255)', rotation=0, labelpad=10)
