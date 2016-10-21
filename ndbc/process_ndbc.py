# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 17:15:53 2016

@author: Bradley

Processing NDBC buoy wave data.
Use get_ndbc.py to retrieve data.
Use plot_ndbc_1.py to plot data.

"""

# import modules
import os
import sys
alp = os.path.abspath('../../LiveOcean/alpha')
if alp not in sys.path:
    sys.path.append(alp)
import zfun
import pickle
import numpy as np
import pandas as pd
from warnings import filterwarnings
filterwarnings('ignore')  # skip some warning messages

# select directory
which_home = os.environ.get("HOME")  # Mac version
if which_home == '/Users/PM5':
    dirname = which_home + 'Documents/tools_data/obs_data/ndbc/'
elif which_home == '/home/parker':
    dirname = '/data1/parker/tools_data/obs_data/ndbc/'
elif which_home == '/home/bbartos':
    dirname = which_home + '/tools_data/obs_data/ndbc/'
elif which_home is None:  # Windows version
    which_home = os.path.expanduser("~")
    dirname = (which_home.replace('\\', '/') +
               '/Documents/Research Work/Parker/tools_data/obs_data/ndbc/')
else:
    print('Trouble filling out environment variables')

# **** USER EDITS ****

# Specify NDBC buoy stations

# Washington and Oregon (from Puget Sound to S. Oregon)
#sn_list = ['wpow1','sisw1','46088','46087','ttiw1','desw1','46041']
#sn_list = ['46029','46089','46005','nwpo3','46050','46015','46002']

# For LiveOcean Comparison
sn_list = ['46088', '46087', '46041', '46029', '46089', '46050']

# Entire West Coast
#sn_list = ['wpow1', 'sisw1', 'ttiw1', 'desw1', 'nwpo3', 'ptac1', 'ptgc1',
#           '46088', '46087', '46041', '46029', '46089', '46005', '46050',
#           '46015', '46002', '46027', '46022', '46006', '46014', '46013',
#           '46059', '46026', '46012', '46024', '46028', '46011', '46053',
#           '46054', '46069', '46025', '46047', '46086']

# Testing
#sn_list = ['46088','46041']

# Time filters
#    m = month
#    w = week
#    d = day
tf_list = ['m', 'w', 'd']

# Load and process NDBC Buoy Data

"""
For desw1, nwpo3, sisw1, ttiw1, wtpo1, 46088, 46087, 46041, 46089, 46005, 46050,
46015, 46002 the columns are:

1984-1993:
YY MM DD hh WD   WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS

1994-1995:
YY MM DD hh WD   WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS\r

1996-1997:
YY MM DD hh WD   WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS

1998:
YY MM DD hh WD   WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS
98 01 01 00 172  8.2  8.9 99.00 99.00 99.00 999 1011.4   8.7 999.0   6.9 99.0\r

1999:
YYYY MM DD hh WD   WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS
1999 01 01 00  69  4.5  6.1 99.00 99.00 99.00 999 1021.6   7.6 999.0   4.8 99.0\r

2000-2004:
YYYY MM DD hh WD   WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS  TIDE

2005-2006:
YYYY MM DD hh mm  WD  WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS  TIDE

2007-2015: (but 2008 and 2010 had deg instead of degT for MWD,
            and 2007, 2008, and 2010 had nmi instead of mi for VIS)
#YY  MM DD hh mm WDIR WSPD GST  WVHT   DPD   APD MWD   PRES  ATMP  WTMP  DEWP  VIS  TIDE
#yr  mo dy hr mn degT m/s  m/s     m   sec   sec degT   hPa  degC  degC  degC   mi    ft
"""
"""
For 46029 the columns are:

1984-1993:
YY MM DD hh WD   WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS

1994-1995:
YY MM DD hh WD   WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS\r

1996-1997:
YY MM DD hh WD   WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS

1998:
YY MM DD hh WD   WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS
98 01 01 00 172  8.2  8.9 99.00 99.00 99.00 999 1011.4   8.7 999.0   6.9 99.0\r

1999:
YYYY MM DD hh WD   WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS
1999 01 01 00  69  4.5  6.1 99.00 99.00 99.00 999 1021.6   7.6 999.0   4.8 99.0\r

2000-2003:
YYYY MM DD hh WD   WSPD GST  WVHT  DPD   APD  MWD  BAR    ATMP  WTMP  DEWP  VIS  TIDE

2004-2015: (but 2004, 2005, 2006, 2008 and 2010 had deg instead of degT for MWD, 
            and 2007, 2008, and 2010 had nmi instead of mi for VIS)
#YY  MM DD hh mm WDIR WSPD GST  WVHT   DPD   APD MWD   PRES  ATMP  WTMP  DEWP  VIS  TIDE
#yr  mo dy hr mn degT m/s  m/s     m   sec   sec deg   hPa  degC  degC  degC   mi    ft
"""


def get_data(fn, tf_list, yr):
# Read the txt file into a Dataframe
    if sn == '46029':
        if yr in range(1984, 1999):  # 2-digit year: use %y
            df = pd.read_csv(fn, delim_whitespace=True, index_col='date',
                             parse_dates={'date': [0, 1, 2, 3]},
                             date_parser=lambda x: pd.datetime.strptime(x,'%y %m %d %H'))
        if yr in range(1999, 2004):
            df = pd.read_csv(fn, delim_whitespace=True, index_col='date',
                             parse_dates={'date':[0, 1, 2, 3]},
                             date_parser=lambda x: pd.datetime.strptime(x,'%Y %m %d %H'))
        elif yr >= 2004:  # add minutes column
            df = pd.read_csv(fn, delim_whitespace=True, index_col='date',
                             skiprows=[1],
                             parse_dates={'date':[0, 1, 2, 3, 4]},
                             date_parser=lambda x: pd.datetime.strptime(x,'%Y %m %d %H %M'))
    else:
        if yr in range(1984, 1999): # 2-digit year: use %y
            df = pd.read_csv(fn, delim_whitespace=True, index_col='date',
                             parse_dates={'date':[0, 1, 2, 3]},
                             date_parser=lambda x: pd.datetime.strptime(x,'%y %m %d %H'))
        if yr in range(1999, 2005): # switch to 4-digit year: use %Y
            df = pd.read_csv(fn, delim_whitespace=True, index_col='date',
                             parse_dates={'date':[0, 1, 2, 3]},
                             date_parser=lambda x: pd.datetime.strptime(x,'%Y %m %d %H'))
        elif yr >= 2005: # add minutes column
            df = pd.read_csv(fn, delim_whitespace=True, index_col='date',
                             skiprows=[1],
                             parse_dates={'date':[0, 1, 2, 3, 4]},
                             date_parser=lambda x: pd.datetime.strptime(x,'%Y %m %d %H %M'))
    df = df.rename(columns={'WD': 'WDIR', 'BAR': 'PRES'})
    
    # mask known missing data
    df[df==9999.0] = np.nan
    df[df==999.0] = np.nan
    df[df==99.0] = np.nan
    
    # fix some obviously bad data
    if fn == '46002h2015.txt':
        df[5800:6250] = np.nan
        
# Create wind time series
    # WSPD is in m/s and WDIR is the compass direction
    # that the wind is coming FROM

    # create 10m standard WSPD
    P = 0.11
    z_stnd = 10
    z_meas = 5
    df['WSPD_10'] = df['WSPD'] * (z_stnd/z_meas)**P

    # create directional WSPD
    wspd_10 = df.WSPD_10.values
    wdir = df.WDIR.values
    theta = 1.5*np.pi - np.pi*wdir/180.
    U_WSPD = wspd_10 * np.cos(theta)
    V_WSPD = wspd_10 * np.sin(theta)
    df['Uwind'] = U_WSPD; df['Vwind'] = V_WSPD

# Create wind stress
    Cd = 0.0013
    rho_air = 1.22
    tau = Cd * rho_air * wspd_10**2
    taux = tau * np.cos(theta)
    tauy = tau * np.sin(theta)
    df['taux'] = taux
    df['tauy'] = tauy

    return df

# Retrieval
yr_list = range(1984,2016)
ndbc_df_m = dict()
ndbc_df_w = dict()
ndbc_df_d = dict()
ndbc_clim = dict()
ndbc_clim_std = dict()
for sn in sn_list:
    id_list = []
    count = 0
    for yr in yr_list: 
        id = str(sn) + 'h' + str(yr)
        id_list.append(id)
        fn = ('C:/Users/Bradley/Documents/Research Work/Parker/tools_data/obs_data/ndbc/'
                + sn + '/' + id + '.txt')
        try:
            dff = get_data(fn, tf_list, yr)
            print(fn + ' = success')
            if count == 0:
                DFF = dff
                count += 1
            else:
                DFF = DFF.append(dff)
        except OSError:
            print(fn + ' = fail')
            pass

# Time filters
    # change to hour sampling, filling time gaps
    DFF = DFF.resample('H', how='mean')
    DFF = DFF.reindex(pd.date_range(DFF.index[1], DFF.index[-1], freq='H')) 
    day_limit = 2 # fills gaps up to this number of days
    DFF_inter = DFF.interpolate(method='linear', limit=24*day_limit)    
    
    # create arrays for filtering
    DFF_array = DFF.as_matrix()
    DFF_header = DFF.columns.values
    
    # godin filter
    filt_array = np.array(DFF_array)
    for j in range(DFF_array.shape[1]):
        filt_array[:,j] = zfun.filt_godin(DFF_array[:,j])
        
    # hanning filter
    for tf in tf_list:
        if tf == 'm':
            filt_m = np.array(DFF_array)
            for j in range(filt_array.shape[1]):
                filt_m[:,j] = zfun.filt_hanning(filt_array[:,j], n=720)
        elif tf == 'w':
            filt_w = np.array(DFF_array)
            for j in range(filt_array.shape[1]):
                filt_w[:,j] = zfun.filt_hanning(filt_array[:,j], n=168)
        elif tf == 'd':
            pass
        
    # reform dataframes
    DFF_m = pd.DataFrame(filt_m, index=DFF.index, columns=DFF_header)
    DFF_w = pd.DataFrame(filt_w, index=DFF.index, columns=DFF_header)
    DFF_d = pd.DataFrame(filt_array, index=DFF.index, columns=DFF_header)

# Climatology with Standard Deviation
    clim_DFF = pd.DataFrame(index = np.arange(1,54), columns = DFF_d.columns)
    clim_std_DFF = pd.DataFrame(index = np.arange(1,54), columns = DFF_d.columns)
    for w in np.arange(1,54):
        DFFmask = DFF_d[DFF_d.index.week == w]
        clim_DFF.ix[w] = np.nanmean(DFFmask, axis=0)
        clim_std_DFF.ix[w] = np.nanstd(DFFmask, axis=0)
    # Dataframes have index of ordinal weeks, convert to date range using
    # clim_DFF.index = pd.date_range(start='', periods=len(clim_DFF),freq='W')
    # with starting year as start, ie. '2014'.

# Save dataframes to dictionaries
    ndbc_df_m[sn] = DFF_m
    ndbc_df_w[sn] = DFF_w
    ndbc_df_d[sn] = DFF_d
    ndbc_clim[sn] = clim_DFF
    ndbc_clim_std[sn] = clim_std_DFF

# Save dictionaries
fn_m = open(os.path.join(dirname,'ndbc_df_m.txt'),'wb')
pickle.dump(ndbc_df_m, fn_m)
fn_w = open(os.path.join(dirname,'ndbc_df_w.txt'),'wb')
pickle.dump(ndbc_df_w, fn_w)
fn_d = open(os.path.join(dirname,'ndbc_df_d.txt'),'wb')
pickle.dump(ndbc_df_d, fn_d)

fn_clim = open(os.path.join(dirname,'ndbc_clim_df.txt'),'wb')
pickle.dump(ndbc_clim, fn_clim)
fn_clim_std = open(os.path.join(dirname,'ndbc_clim_std_df.txt'),'wb')
pickle.dump(ndbc_clim_std, fn_clim_std)

# Unit dictionary
header = pd.read_csv(fn, nrows=1, delim_whitespace=True)
unit_dict = dict(header.ix[0])
unit_dict['taux'] = 'Pa'
unit_dict['tauy'] = 'Pa'
unit_dict['WSPD_10'] = unit_dict['WSPD']
unit_dict['Uwind'] = unit_dict['WSPD']
unit_dict['Vwind'] = unit_dict['WSPD']

fn_head = open(os.path.join(dirname,'ndbc_unit_dict.txt'),'wb')
pickle.dump(unit_dict, fn_head)
