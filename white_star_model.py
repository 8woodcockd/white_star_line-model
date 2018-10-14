# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 19:37:18 2018

@author: Dean
"""
import csv
import terrain
import matplotlib.pyplot
import matplotlib.colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.patches
import os

tuggable_mass = 36000000
fraction_ice_asl = 0.1 # Fraction of ice column above surface.
resolution = 1
pixel_area = resolution**2
ice_mass_density = 900 # 900kg per cubic meter.
lidar_unit_height = 0.1    # One unit in the lidar data represents 0.1m height.
radar_texture_filter = 100  # Values >= to this are interpreted as ice.


def plot_input(radar, lidar, cols_radar, filename1, filename2):
    """This function will produce an output map showing the positions of 
    icebergs with an assigned identifcation number, and their attributes 
    (mass and volume).
    """
    # Generate two subplots to display input radar and lidar data.
    fig, (ax1, ax2) = matplotlib.pyplot.subplots(1, 2, figsize=(15, 10))
    fig.suptitle('Input Radar and Lidar Data')
    
    # Create plot of input radar data.
    c1 = ax1.imshow(radar, cmap=matplotlib.pyplot.cm.get_cmap('Blues'))
    ax1.set_title('Radar:', x=0, y=1.05, ha='left')
    ax1.set_ylabel('Distance (m)')
    ax1.tick_params(labelbottom=False, labeltop=True, top = True, right=True)
    # Customise x-label definition and position.
    ax1.text((cols_radar / 2), -20, 'Distance (m)', fontsize=10,
            horizontalalignment='center', verticalalignment='center')
    
    # Create plot of input lidar data.
    c2 = ax2.imshow(lidar, cmap=matplotlib.pyplot.cm.get_cmap('Reds'))
    ax2.set_title('Lidar:', x=0, y=1.05, ha='left')
    ax2.set_ylabel('Distance (m)')
    ax2.tick_params(labelbottom=False, labeltop=True, top=True, right=True)
    # customised y-label definition and position
    ax2.text((cols_radar / 2), -20, 'Distance (m)', fontsize=10,
            horizontalalignment='center', verticalalignment='center')
    
    # Position colourbar 1 next to axes 1.
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes('bottom', size='5%', pad=0.1)
    cbar1 = fig.colorbar(c1, orientation="horizontal", cax=cax)
    cbar1.set_label('Value (0-255)', rotation=0, labelpad=10)
    
    # Position colourbar 2 next to axes 2.
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes('bottom', size='5%', pad=0.1)
    cbar2 = fig.colorbar(c2, orientation="horizontal", cax = cax)
    cbar2.set_label('Value (0-255)', rotation=0, labelpad=10)
    
    # Check if the 'Model_Outputs folder exists to save the out put map inside.
    # Create it if it does not exist.
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'Model_Outputs')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    # Save figure as an image, creating a name from the input files used.
    save_1 = filename1.rsplit(".",1)[0]
    save_2 = filename2.rsplit(".",1)[0]
    fig.savefig('Model_Outputs/' + str(save_1) + '_&_' + str(save_2) + 
                '_input' + '.png')  
    fig.show()
# The running_model function is called when the run button in the GUI is 
# pressed or the cose at the bottom of the script can be uncommented in order 
# to run this script directly and call this function.
#run_program = False
def running_model(P1, P2, filename1, filename2, plot_inputs):
    """Process the input radar and lidar data and determine the position and
    attributes of each iceberg within the area of interest.
    """
    
    # Load the radar data.
    radar = []
    with open(P1, newline='') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader: 
            rowlist = []
            for value in row:
                rowlist.append(value)
            radar.append(rowlist)
    # Calculate the number of x and y values and hence the grid area. The lidar 
    # data area should be for exatly the same area and be at exactly the same 
    # resoltion (1m).
    rows_radar = len(radar)
    cols_radar = len(radar[0])
    
    # Load the lidar data.
    lidar = []
    with open(P2, newline='') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader: 
            #print(row)
            rowlist = []
            for value in row:
                rowlist.append(value)
            lidar.append(rowlist)
    
    # Show plots of input radar and lidar data if user has chosen to plot this.
    if plot_inputs == True:
        plot_input(radar,lidar,cols_radar, filename1, filename2)    

    # Classify the terrain of each square meter area in the grid area as either 
    # ice or sea. From this create grid showing ice reference numbers in the 
    # position of each ice cell in the list of ice. This is then used to 
    # efficiently identify and find neighbouring ice cells by their reference
    # number.
    ice = []
    sea = []
    ice_ref = []
    ref = 0
    for i in range (rows_radar):
        ice_ref_row = []
        for j in range (cols_radar):
            if radar[i][j] >= 100: 
                ice.append(terrain.Ice(i, j, radar, lidar, lidar_unit_height, 
                                       pixel_area, ice_mass_density, 
                                       fraction_ice_asl, cols_radar))
                ice_ref_row.append(ref)
                ref += 1
            else:
                sea.append(terrain.Sea(i, j, radar, lidar))
                ice_ref_row.append(-1)
        ice_ref.append(ice_ref_row)
    print('number of cells (sq m) containing ice:', len(ice))
    print('number of cells (sq m) not containing ice:', len(sea))
    
    # Identify and create a list of each ice cells neighbours that are also
    # ice to enable the identification of icebergs (groups of ice cells).
    # A list of each ice cells neighbours is appended to each ice cell.
    for i in range (len(ice)):
        # cell to the north
        if radar[ice[i].y - 1][ice[i].x] >= 100:
            ice[i].neighbours.append(ice[ice_ref[ice[i].y - 1][ice[i].x]]) 
        # cell to the west
        if radar[ice[i].y][ice[i].x - 1] >= 100:
            ice[i].neighbours.append(ice[ice_ref[ice[i].y][ice[i].x - 1]])
        # cell to the south
        if radar[ice[i].y + 1][ice[i].x] >= 100:
            ice[i].neighbours.append(ice[ice_ref[ice[i].y + 1][ice[i].x]])
        # cell to the east
        if radar[ice[i].y][ice[i].x + 1] >= 100:
            ice[i].neighbours.append(ice[ice_ref[ice[i].y][ice[i].x + 1]])
    
    # Loop through all ice not in the 'checked' list and keep adding the  
    # neighbouring ice cells to the 'to_check' list as they are part of the 
    # same iceberg. When the 'to_check list becomes empty a new loop begins 
    # which will seek the next group of ice cells that make up an iceberg and 
    # assign them all the same ID number.     
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
            while len(to_check) > 0:
                to_check[0].id = id
                for j in range(len(to_check[0].neighbours)):
                    if (to_check[0].neighbours[j] not in checked) & (
                            to_check[0].neighbours[j] not in to_check):
                        to_check.append(to_check[0].neighbours[j])
                checked.append(to_check[0])
                to_check.remove(to_check[0])
    
    # Record the number of icebergs within the data area.            
    num_of_icebergs = id
    print('number of icebergs:', num_of_icebergs)
    
    # Calculate the total mass of ice in each iceberg.
    iceberg_mass = []
    for i in range(num_of_icebergs):
        berg_mass = 0
        for j in range (len(ice)):
            if ice[j].id == i + 1:
                berg_mass += ice[j].mass_tot
        iceberg_mass.append(berg_mass)
        
    # Calculate the total volume of ice in each iceberg.
    iceberg_volume = []
    for i in range(num_of_icebergs):
        berg_volume = 0
        for j in range (len(ice)):
            if ice[j].id == i + 1:
                berg_volume += ice[j].volume_tot
        iceberg_volume.append(berg_volume)
    
    
    # Check if the 'Model_Outputs folder exists to save the out put map inside.
    # Create it if it does not exist.
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'Model_Outputs')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    
    # Print the results of which icebergs can be tugged and which cannot.
    can_tug = []
    with open ("Model_Outputs/Iceberg_details.txt", "w") as f:
        for i in range(num_of_icebergs):
            if iceberg_mass[i] < tuggable_mass:
                print('Iceberg {0} can be tugged (mass = {1}kg, '\
                      'volume = {2}m^3)'
                     .format(str(i + 1), int(iceberg_mass[i]), 
                             int(iceberg_volume[i])))
                f.write('Iceberg {0} can be tugged (mass = {1}kg, '\
                        'volume = {2}m^3)\n'
                     .format(str(i + 1), int(iceberg_mass[i]), 
                             int(iceberg_volume[i])))
                can_tug.append(i + 1)
            else:
                print('Iceberg {0} cannot be tugged (mass = {1}kg, '\
                      'volume = {2}m^3)'
                      .format(str(i + 1), int(iceberg_mass[i]), 
                              int(iceberg_volume[i])))
                f.write('Iceberg {0} cannot be tugged (mass = {1}kg, '\
                        'volume = {2}m^3)\n'
                      .format(str(i + 1), int(iceberg_mass[i]), 
                              int(iceberg_volume[i]))) 
            
    # Alter the property of each ice cell depending on whether it is part of an 
    # iceberg that can be tugged or not.
    for i in range(len(ice)):
        if ice[i].id in can_tug:
            ice[i].tug = True         
    
    # Create a rastor layer that can plot icebergs and differentiate between 
    # those that can be tugged and those that cannot.
    tug_mask = []
    for i in range(rows_radar):
        tug_mask_row = []
        for j in range(cols_radar):
            if radar[i][j] < 100:
                tug_mask_row.append(0)
            elif ice[ice_ref[i][j]].tug == False:         
                tug_mask_row.append(2)
            elif ice[ice_ref[i][j]].tug == True:
                tug_mask_row.append(1)  
        tug_mask.append(tug_mask_row)
    
    # Generate a figure showing iceberg positions in the area of interest.
    fig2 = matplotlib.pyplot.figure(figsize=(16, 13))
    fig2.suptitle('White Star Line Iceberg Model')
    cmap_iceberg = matplotlib.colors.ListedColormap(['blue', 'green', 'red'])
    matplotlib.pyplot.imshow(tug_mask, cmap=cmap_iceberg)
    
    # Create a custom legend to label the  whether the iceberg can be tugged or
    # not and which areas are not ice (assumed sea).
    class_sea = matplotlib.patches.Patch(color='blue', label='Sea')
    class_tuggable_iceberg = matplotlib.patches.Patch(color='green', 
                                            label='Tuggable iceberg')
    class_non_tuggable_iceberg = matplotlib.patches.Patch(color='red', 
                                                label='Non-tuggable iceberg')
    ax = matplotlib.pyplot; ax.ticklabel_format(useOffset=False, style='plain')
    ax.legend(handles=[class_sea, class_tuggable_iceberg,
                       class_non_tuggable_iceberg],
              handlelength=0.7, bbox_to_anchor=(1.05, 0.4), loc='lower left',
              borderaxespad=0.)
    ax.tick_params(labelbottom=False, labeltop=True, top = True, right = True)
    matplotlib.pyplot.ylabel('Distance (m)')
    # Customised x-label definition and position.
    ax.text((cols_radar / 2), -20, 'Distance (m)', fontsize=10,
            horizontalalignment='center', verticalalignment='center')
    
    # Find the first coordinate of each iceberg and insert ID labels at this
    # position.
    label_coords = []
    for i in range(num_of_icebergs):
        for j in range(len(ice)):
            if ice[j].id == i + 1:
                label_coords.append([ice[j].x, ice[j].y])
                props = dict(boxstyle='round', facecolor='ghostwhite', alpha=1)
                ax.text(
                        ice[j].x, ice[j].y, 'Iceberg {0}\n(mass = {1}kg)\n'\
                        '(volume = {2}m^3)'
                        .format((i + 1), int(iceberg_mass[i]), 
                                int(iceberg_volume[i])), fontsize=10,
                                horizontalalignment='right', 
                                verticalalignment='bottom', bbox = props, 
                                alpha=0.5, 
                                wrap = True)
                break
        
    
    # Check if the 'Model_Outputs folder exists to save the out put map inside.
    # Create it if it does not exist.
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'Model_Outputs')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    # Save figure as an image, creating a name from the input files used.
    save_1 = filename1.rsplit(".",1)[0]
    save_2 = filename2.rsplit(".",1)[0]
    fig2.savefig('Model_Outputs/' + str(save_1) + '_&_' + str(save_2) +
                 '_output' + '.png')    
    fig2.show()
    print('\nModel run complete.')