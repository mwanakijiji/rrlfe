#!/usr/bin/env python
# coding: utf-8

# This plots the epochs at which RR Lyrae spectra were taken

# created 2017 Dec 19 by E.S.

import astropy
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
from datetime import datetime
from astropy import time, coordinates as coord, units as u
from astropy.time import Time
from dateutil.parser import parse

stem = "/Users/bandari/Documents/git.repos/rrlfe/" + \
"src/mcdonald_spectra/original_fits_files/"

import os
arr_files = os.listdir(stem) # list files

# read in each FITS file in the directory and obtain epoch, coords from header

fileList = []
dateList = []
epochList = []
raList = []
decList = []

for f in range(0,len(arr_files)): # loop over filenames

    # retrieve header
    image, header = fits.getdata(stem+arr_files[f],
                                     0,
                                     header=True)

    # observation epoch
    epoch = header['DATE-OBS']+' '+header['UT']
    obj = header['OBJECT']
    ra = header['RA']
    dec = header['DEC']

    # parse
    epoch_dateTime = datetime.strptime(epoch, '%Y-%m-%d %H:%M:%S.%f')
    fileList.append(arr_files[f])
    dateList.append(epoch_dateTime)
    epochList.append(epoch)
    raList.append(ra)
    decList.append(dec)


ut_list = {'file':fileList,'ut_epoch':epochList,'ra':raList,'dec':decList, }

df_ut = pd.DataFrame(ut_list)

loc_mcdonald = coord.EarthLocation.from_geodetic(lon=-104.0215753,lat=30.6715396,height=2076,ellipsoid='WGS84')

# convert UTC times to isot format, then compile into list of astropy Time object
t_spectra_iso = [Time(dateList[i].isoformat(), format='isot', scale='utc') for i in range(len(dateList))]

# convert isot-format times to JD
t_spectra_jd = [t_spectra_iso[i].jd for i in range(len(t_spectra_iso))]

# put JDs into dataframe
df_ut["jd"] = t_spectra_jd

# combine all data for across-the-board comparison
allFileList = np.hstack((fileList,fileList))
allSpecEpochList_utc = np.hstack((dateList,dateList))
allSpecEpochList_jd = np.hstack((t_spectra_jd,t_spectra_jd))
#allSpecEpochList_bjd = np.hstack((t_spectra_2012_bjd,t_spectra_2013_bjd))

# convert JD to BJD
def convert_jd_to_bjd(jdTimes,observatoryLoc,skyCoordObj):

    timesObj = time.Time(jdTimes, format='jd', scale='utc', location=observatoryLoc)
    ltt_bary = timesObj.light_travel_time(skyCoordObj)

    time_barycentre = timesObj.tdb + ltt_bary

    return time_barycentre

# star names as they appear in the filenames
'''
star_names_files = ['RW_Ari','X_Ari','UY_Cam','RR_Cet','SV_Eri',
              'VX_Her','RR_Leo','TT_Lyn','TV_Lyn','TW_Lyn',
              'RR_Lyr','V_535','V445','AV_Peg','BH_Peg',
              'AR_Per','RU_Psc','T_Sex','TU_UMa']

# star names for SIMBAD lookup
star_names_simbad = ['RW Ari','X Ari','UY Cam','RR Cet','SV Eri',
              'VX Her','RR Leo','TT Lyn','TV Lyn','TW Lyn',
              'RR Lyr','V535 Mon','V445 Oph','AV Peg','BH Peg',
              'AR Per','RU Psc','T Sex','TU UMa']
'''

# initialize
df_ut["bjd"] = np.nan

# find BJDs and concatenate everything into one dataframe

dfAll = pd.DataFrame()

for spec_num in range(0,len(df_ut)):
    jd_this_spec = df_ut["jd"].loc[spec_num]
    ra_this_spect = df_ut["ra"].loc[spec_num]
    dec_this_spect = df_ut["dec"].loc[spec_num]
    coords_this_spect = str(ra_this_spect + " " +dec_this_spect)

    coord_thisStar = coord.SkyCoord(coords_this_spect, frame='icrs', unit=(u.hourangle, u.deg))

    bjd_this_spec = convert_jd_to_bjd(jdTimes=jd_this_spec,
                      observatoryLoc=loc_mcdonald,
                      skyCoordObj=coord_thisStar)

    df_ut["bjd"].loc[spec_num] = bjd_this_spec

    '''
    df_this_spec = return_star_bjds(fileNames=dfAll["filenames"].loc[spec_num],
                                    allSpecEpochList_jd=dfAll[""].loc[spec_num],
                                    star_names_files[star],
                                    star_names_simbad[star],
                                    loc_mcdonald)
    '''
    '''
    dfAll = pd.concat([dfAll,df_thisStar])
    '''
# fileNames,jdTimes,starNameFile,starNameGeneric,observatoryLoc

'''
for star in range(0,len(star_names_files)):
    df_thisStar = return_star_bjds(allFileList,allSpecEpochList_jd,star_names_files[star],star_names_simbad[star],loc_mcdonald)
    dfAll = pd.concat([dfAll,df_thisStar])
'''


# In[30]:


# write filenames, spectra epochs out csv
output_file_name = './data/junk.csv'
df_ut.to_csv(output_file_name)
print("Wrote ", output_file_name)
