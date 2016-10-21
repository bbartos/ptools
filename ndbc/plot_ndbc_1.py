# -*- coding: utf-8 -*-
"""
Plot NDBC buoy wave data.
Use get_ndbc.py to retrieve data.
Use process_ndbc.py to process data.

"""

# import modules
import os
import pickle
import matplotlib.pyplot as plt
from datetime import datetime
from warnings import filterwarnings
filterwarnings('ignore') # skip some warning messages

plt.close('all')

# Open dictionaries from process_ndbc.py
which_home = os.environ.get("HOME") # Mac version
if which_home == '/Users/PM5':
    dirname = which_home + '/Documents/tools_data/obs_data/ndbc/'
    savname = which_home + '/Documents/ptools_output/ndbc/'
elif which_home == '/home/parker':
    dirname = '/data1/Parker/tools_data/obs_data/ndbc/'
    savname = '/data1/Parker/ptools_output/ndbc/'
elif which_home == '/home/bbartos':
    dirname = which_home + '/tools_data/obs_data/ndbc/'
    savname = which_home + '/ptools_output/ndbc/'
elif which_home == None: # Windows version
    which_home = os.path.expanduser("~")
    dirname = which_home.replace('\\','/') + '/Documents/Research Work/Parker/tools_data/obs_data/ndbc/'
    savname = which_home.replace('\\','/') + '/Documents/Research Work/Parker/ptools_output/ndbc/'
else:
    print('Trouble filling out environment variables')

# choose time filtering length (a string) e.g.:
#    m = month
#    w = week
#    d = day
tf = 'w'

# set time limits 
if False: # plot the full record of data I downloaded
    t0 = datetime(1984,1,1)
    t1 = datetime(2015,12,31)
else: # or select a smaller time span, like a year
    t0 = datetime(2013,1,1)
    t1 = datetime(2015,12,31)

# load data
f = open(os.path.join(dirname,'ndbc_df_' + tf + '.txt'),'rb')
ndbc_df = pickle.load(f)
sn_list = ndbc_df.keys()

f2 = open(os.path.join(dirname,'ndbc_unit_dict.txt'),'rb')
unit_dict = pickle.load(f2)

# construct figure with subplots
NC = 4
NR = len(ndbc_df)
fig, axes = plt.subplots(nrows=NR, ncols=NC, figsize=(30,18))
plt.subplots_adjust(left=0.05, right=0.95, top=0.95)
cc = 0

for sn in ndbc_df:        
# retrieve data from dictionary
    DFF = ndbc_df[sn]
    
# set subplot index
    ir = cc
    cc += 1
    
    for ic in range(NC):
        ax = axes[ir,ic]
            
# WSPD column
        if ic==0: 
            vn = 'WSPD'
            DFF[vn].plot(ax=ax, xlim=(t0,t1), ylim=(0, 15), color='r')
            ax.text(.05, .75, 'NDBC Station ' + str(sn), transform=ax.transAxes)
            if ir==0:
                ax.set_title(vn+' ['+unit_dict[vn]+']')
                ax.set_xticklabels([])
            if ir==(NR-1):
                ax.set_xlabel('Year')
            else:
                ax.set_xlabel('')
                ax.set_xticklabels([])
        
# Tau_y column
        if ic==1:
            vn = 'tauy'
            DFF[vn].plot(ax=ax, xlim=(t0,t1), ylim=(-.1, .2))
            if ir==0:
                ax.set_title(vn+' ['+unit_dict[vn]+']')
                ax.set_xticklabels([])
            if ir==(NR-1):
                ax.set_xlabel('Year')
            else:
                ax.set_xlabel('')
                ax.set_xticklabels([])

# Tau_x column
        if ic==2:
            vn = 'taux'
            DFF[vn].plot(ax=ax, xlim=(t0,t1), ylim=(-.1, .2))
            if ir==0:
                ax.set_title(vn+' ['+unit_dict[vn]+']')
                ax.set_xticklabels([])
            if ir==(NR-1):
                ax.set_xlabel('Year')
            else:
                ax.set_xlabel('')
                ax.set_xticklabels([])
            
        
# Temperature column
        if ic==3:
            vn = 'ATMP'
            DFF[vn].plot(ax=ax, xlim=(t0,t1), ylim=(0, 20))
            vn2 = 'WTMP'
            DFF[vn2].plot(ax=ax, xlim=(t0,t1), ylim=(0, 20), linestyle='--')
            if ir==0:
                ax.set_title(vn+' and '+vn2+' ['+unit_dict[vn]+']')
                ax.set_xticklabels([])
            if ir==(NR-1):
                ax.set_xlabel('Year')
            else:
                ax.set_xlabel('')
                ax.set_xticklabels([])

#plt.show()
#plt.savefig(savname + 'Compare_2.png', bbox_inches='tight')