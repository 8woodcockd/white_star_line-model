# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 19:37:18 2018

@author: Dean
"""
import csv
import terrain
import matplotlib.pyplot
import matplotlib.colors

#filename1 = 'white2_radar.csv'
#filename2 = 'white2_lidar.csv'

tuggable_mass = 36000000
fraction_ice_asl = 0.1 #fraction of ice column above surface
resolution = 1
pixel_area = resolution**2
ice_mass_density = 900 # 900kg per cubic meter
lidar_unit_height = 0.1     # 1 unit in the lidar data represents 0.1m height
radar_texture_filter = 100  # only values greater than or equal to this will be 
                            # considered to indicate the presence of ice

#the main model function is called when the run button in the GUI is pressed.
def running_model(filename1,filename2):

    # load the radar data.
    radar = []
    #with open('white2_radar.txt', newline ='') as f:
    with open(filename1, newline ='') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader: 
            rowlist = []
            for value in row:
                rowlist.append(value)
            radar.append(rowlist)
    #calculate the number of x and y values and hence the grid area. The lidar 
    #data area should be for exatly the same area and be at exactly the same 
    #resoltion (1m)
    rows_radar = len(radar)
    cols_radar = len(radar[0])
    
    # load the lidar data.
    lidar = []
    with open(filename2, newline ='') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader: 
            #print(row)
            rowlist = []
            for value in row:
                rowlist.append(value)
            lidar.append(rowlist)
    
    # classify the terrain of each square meter area in the grid area and 
    # create grid of original data showing position of ice by its reference 
    # position in the ice list. This is to be used to efficiently find 
    # neighbours.
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
                                       fraction_ice_asl))
                ice_ref_row.append(ref)
                ref += 1
            else:
                sea.append(terrain.Sea(i, j, radar, lidar))
                ice_ref_row.append(-1)
        ice_ref.append(ice_ref_row)
    print('number of cells (sq m) containing ice:', len(ice))
    print('number of cells (sq m) not containing ice:', len(sea))
    
    # Identify and create a list of each ice cells neighbouring cells that are 
    # also ice to enable the identification of icebergs (groups of ice cells)
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
    
    # this should loop through all ice not in checked list and keep adding the  
    # neighbours to check to the to_check list and keep working through the ice  
    # in the to check list until it is empty.    
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
                    if (to_check[0].neighbours[j] not in checked) & (
                        to_check[0].neighbours[j] not in to_check):
                        to_check.append(to_check[0].neighbours[j])
                checked.append(to_check[0])
                to_check.remove(to_check[0])
    
    # Record number of icebergs within the data area            
    num_of_icebergs = id
    print('number of icebergs:',num_of_icebergs)
    
    # Calculate the total mass of ice in each iceberg
    iceberg_mass = []
    for i in range(num_of_icebergs):
        berg_mass = 0
        for j in range (len(ice)):
            if ice[j].id == i + 1:
                berg_mass += ice[j].mass_tot
        iceberg_mass.append(berg_mass)
        
    # Calculate the total volume of ice in each iceberg
    iceberg_volume = []
    for i in range(num_of_icebergs):
        berg_volume = 0
        for j in range (len(ice)):
            if ice[j].id == i + 1:
                berg_volume += ice[j].volume_tot
        iceberg_volume.append(berg_volume)
    
    # Print the results of which icebergs can be tugged and which cannot.
    can_tug = []
    with open ("Iceberg_details.txt", "w") as f:
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
            
        
    # alter the property of each ice cell depending on whether it is part of an 
    # iceberg that can be tugged or not
    for i in range(len(ice)):
        if ice[i].id in can_tug:
            ice[i].tug = True         
    
    # create a rastor layer that can plot icebergs and differentiate between 
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
    
    # Generate a afigure showing iceberg positions in area of interest
    fig = matplotlib.pyplot.figure(figsize=(9, 9))
    fig.suptitle('White Star Line Iceberg Model')
    cmap_iceberg = matplotlib.colors.ListedColormap(['blue','green','red'])
    matplotlib.pyplot.imshow(tug_mask,cmap = cmap_iceberg)
    
    # Create custom legend to label the four canopy height classes:
    import matplotlib.patches as mpatches
    class_sea = mpatches.Patch(color='blue', label='Sea')
    class_tuggable_iceberg = mpatches.Patch(color='green', 
                                            label='Tuggable iceberg')
    class_non_tuggable_iceberg = mpatches.Patch(color='red', 
                                                label='Non-tuggable iceberg')
    ax = matplotlib.pyplot; ax.ticklabel_format(useOffset=False, style='plain')
    ax.legend(handles=[class_sea,class_tuggable_iceberg,
                       class_non_tuggable_iceberg],
              handlelength=0.7,bbox_to_anchor=(1.05, 0.4),loc='lower left',
              borderaxespad=0.)
    
    ax.tick_params(labelbottom=False,labeltop=True,top = True, right = True)
    matplotlib.pyplot.ylabel('Distance (m)')
    # ustomised x-label definition and position
    ax.text((cols_radar / 2),-20,'Distance (m)',fontsize=10,
            horizontalalignment='center',verticalalignment='center')
    
    #find first coordinate of each iceberg to position ID labels
    label_coords = []
    for i in range(num_of_icebergs):
        for j in range(len(ice)):
            if ice[j].id == i + 1:
                label_coords.append([ice[j].x, ice[j].y])
                props = dict(boxstyle='round', facecolor='ghostwhite', alpha=1)
                ax.text(
                        ice[j].x, ice[j].y, 'Iceberg {0}\n(mass = {1}kg)\n'\
                        '(volume = {2}m^3)'
                        .format((i + 1),int(iceberg_mass[i]),int(iceberg_volume[i])), 
                        fontsize=10,horizontalalignment='right',
                        verticalalignment='bottom', bbox = props, alpha=0.5, 
                        wrap = True
                        )
                break
    
    print('\nmodel complete')

#running_model(filename1,filename2)