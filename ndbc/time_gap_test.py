# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 18:59:53 2016

@author: Bradley

Determining time gap size in ndbc buoy data.
Use ptools/ndbc/get_ndbc.py for retrieval of ndbc data.
Use ptools/ndbc/process_ndbc.py for processing ndbc data.
"""

import os
import math
import pickle
import numpy as np
from datetime import datetime
from warnings import filterwarnings
filterwarnings('ignore') # skip some warning messages

# set time limits to plot
t0 = datetime(2013,1,2)
t1 = datetime(2016,8,8)
date_string0 = t0.strftime('%Y.%m.%d')
date_string1 = t1.strftime('%Y.%m.%d')

# Set directories and station list from process_ndbc.py
# Choose time filter
tf = 'w' # 'm', 'w', or 'd'

# Find home directory
which_home = os.environ.get("HOME")
if which_home == '/Users/PM5': # Mac
    dirname = which_home + '/Documents/tools_data/obs_data/ndbc/'
    savname = which_home + '/Documents/LiveOcean_output/ndbc/'
elif which_home == '/home/parker': # Fjord
    dirname = which_home + '/tools_data/obs_data/ndbc/'
    savname = which_home + '/LiveOcean_output/ndbc/'
elif which_home == '/home/bbartos': # Bradley's Fjord
    dirname = which_home + '/tools_data/obs_data/ndbc/'
    savname = which_home + '/LiveOcean_output/ndbc/'
elif which_home == None: # Windows version
    which_home = os.path.expanduser("~")
    dirname = which_home.replace('\\','/') + '/Documents/Research Work/Parker/tools_data/obs_data/ndbc/'
    savname = which_home.replace('\\','/') + '/Documents/Research Work/Parker/LiveOcean_output/ndbc/'
else:
    print('Trouble filling out environment variables')

fn = open(os.path.join(dirname,('ndbc_df_' + tf + '.txt')),'rb')
ndbc_df = pickle.load(fn)

# For standard LiveOcean stations
sn_list = ['46088','46087','46041','46029','46089','46050']
#sn_list = ['46088','46041']

# Begin station loop
nan_dict = dict()
for sn in sn_list:
    print('Working on Station ' + sn + '.')
# Load ndbc data
    try:
        DFF = ndbc_df[sn]

    except:
        print('ndbc data for Station ' + sn + ' and time ' + date_string0 + 
            '_' + date_string1 + ' not found.')
        pass
    c = 2
    cc = 0
    nan_count = np.zeros(200)
    for j in range(len(DFF)):
#        print('Testing time ' + str(DFF.index[j]) + '.')
        if math.isnan(DFF['WSPD'][j])==True and math.isnan(DFF['WSPD'][j-1])==False:
            c = 2
        if math.isnan(DFF['WSPD'][j])==True and math.isnan(DFF['WSPD'][j-1])==True:
#            print('Gap is ' + str(c) + ' hours long.')
            nan_count[cc] = c
            c += 1
        if math.isnan(DFF['WSPD'][j])==False and math.isnan(DFF['WSPD'][j-1])==True:
            print('Previous gap was ' + str(c) + ' hours long.')
            cc += 1
    nan_count = sorted(nan_count, reverse=True)
    nan_dict[sn] = nan_count

