# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 08:06:36 2016

@author: PM5

Code to automate getting multiple years of NDBC buoy data
"""

import os
import sys
alp = os.path.abspath('../../LiveOcean/alpha')
if alp not in sys.path:
    sys.path.append(alp)
import Lfun
import bs4
import urllib.request as U

# Specify which NDBC buoy numbers
#sn_list = ['46027',] # with one buoy: keep square brackets and comma to indicate list
sn_list = ['wpow1','sisw1','ttiw1','desw1','nwpo3','46088','46087','46041','46029','46089',
           '46005','46050','46015','46002'] # Washington and Oregon
#sn_list = ['wpow1','sisw1','ttiw1','desw1','nwpo3','ptac1','ptgc1','46088','46087','46041',
#            '46029','46089','46005','46050','46015','46002','46027','46022','46006','46014',
#            '46013','46059','46026','46012','46024','46028','46011','46053','46054','46069',
#            '46025','46047','46086'] # entire West Coast

           

for sn in sn_list:
# Make a new, clean directory
    which_home = os.environ.get("HOME") # Mac version
    if which_home == '/Users/PM5':
        dirname = which_home + '/Documents/tools_data/obs_data/ndbc/' + sn
    elif which_home == '/home/parker':
        dirname = '/data1/Parker/tools_data/obs_data/ndbc/' + sn
    elif which_home == '/home/bbartos':
        dirname = which_home + '/tools_data/obs_data/ndbc/' + sn
    elif which_home == None: # Windows version
        which_home = os.path.expanduser("~")
        dirname = which_home.replace('\\','/') + '/Documents/Research Work/Parker/tools_data/obs_data/ndbc/' + sn
    else:
        print('Trouble filling out environment variables')
    Lfun.make_dir(dirname, clean=True)

# Retrieve data and save it to the directory
    yr_list = range(1984,2017)

    for yr in yr_list:
        try:
            idn = str(sn) + 'h' + str(yr)
            print('Attempting to get ' + idn)
            url_str = ('http://www.ndbc.noaa.gov/view_text_file.php?filename=' +
                       idn + '.txt.gz&dir=data/historical/stdmet/')
            html = U.urlopen(url_str, timeout=10)
            soup = bs4.BeautifulSoup(html, 'html.parser')
            sn_text = soup.findAll(text=True)
            sns = str(sn_text)[2:-2]
            sns = sns.replace('\\n','\n')
            f = open(os.path.join(dirname,idn + '.txt'),'w')
            f.write(sns)
            f.close()
        except:
            pass


