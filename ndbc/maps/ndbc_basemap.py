# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 18:50:02 2016

For creation of a map of NDBC buoy stations used in the LiveOcean model.

@author: Bradley
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# full station list with locations (station, lat, lon)
sn_loc = np.array([[46088,48.334,-123.165],[46087,48.494,-124.728],[46041,47.353,-124.731],
          [46029,46.159,-124.514],[46089,45.893,-125.819],[46005,45.95,-131],
          [46050,44.656,-124.526],[46015,42.764,-124.832],[46002,42.614,-130.49]])

# list of stations to plot
sn_ltp = [46088,46087,46089,46041,46050,46029] # choose stations here
sn_list = np.zeros([len(sn_ltp),3])
c = 0
for j in range(len(sn_loc)):
    if sn_loc[j,0] in sn_ltp:
        sn_list[c] = sn_loc[j]
        c += 1

# map edges
lat_min = int(float(min(sn_list[:,1]))) - 1
lon_min = int(float(min(sn_list[:,2]))) - 2
lat_max = int(float(max(sn_list[:,1]))) + 2
lon_max = int(float(max(sn_list[:,2]))) + 1

map = Basemap(llcrnrlon=lon_min, llcrnrlat=lat_min, urcrnrlon=lon_max, urcrnrlat=lat_max, projection='cass', lon_0=(lon_max+lon_min)/2, lat_0=(lat_max+lat_min)/2, resolution='i')

# mask with map image
#map.etopo()

# draw coastlines, country boundaries, fill land
map.drawcoastlines(linewidth=1, color='darkgrey')
map.drawstates(linewidth=1, linestyle='--', color='darkgrey')
map.drawcountries(linewidth=1, linestyle='--', color='darkgrey')
map.fillcontinents(color='lightgrey',lake_color='lightblue')

# draw the edge of the map and fill the ocean
map.drawmapboundary(fill_color='lightblue')

# draw lat/lon grid lines 
map.drawmeridians(np.arange(lon_min,lon_max,2), labels=[0,0,0,1])
map.drawparallels(np.arange(lat_min,lat_max,2), labels=[1,0,0,0])

# add station scatterplot
x = sn_list[:,2]
y = sn_list[:,1]
labels = sn_list[:,0]
map.scatter(x, y, s=50, latlon=True, c='r')

# label stations
for j in range(len(sn_list)):
    x_coord, y_coord = map(x[j],y[j])
    plt.text(x_coord, y_coord, int(labels[j]), fontsize=12, fontweight='bold')
    
plt.show()

# find save directory
which_home = os.environ.get("HOME")
#if which_home == '/Users/PM5':
#    dirname = which_home + 'Documents/tools_data/obs_data/ndbc/'
#elif which_home == '/home/parker':
#    dirname = 'Data1/Parker/tools_data/obs_data/ndbc/'
#if which_home == '/home/bbartos':  # Bradley's Fjord
#    dirname = which_home + '/maps/ndbc/'
#elif which_home == None:  # Windows version
#    which_home = os.path.expanduser("~")
#    dirname = which_home.replace('\\','/') + '/Documents/Research Work/Parker/ptools/ndbc/maps/'
#else:
#    print('Trouble filling out environment variables')
#fn = dirname + 'station_map.png'

# save basemap
#plt.savefig(fn)